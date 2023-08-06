/* Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include <cstdint>
#include <limits>
#include <vector>

#include <absl/strings/str_cat.h>

#if HYBRIDBACKEND_SPARSEHASH
#include <sparsehash/dense_hash_map>
#endif

#include <tensorflow/core/framework/common_shape_fns.h>
#include <tensorflow/core/framework/op.h>
#include <tensorflow/core/framework/op_def_builder.h>
#include <tensorflow/core/framework/partial_tensor_shape.h>
#include <tensorflow/core/framework/resource_mgr.h>
#include <tensorflow/core/framework/shape_inference.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/public/version.h>

#include "hybridbackend/common/env.h"

namespace tensorflow {
namespace hybridbackend {

#define TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(m)                     \
  m(int32, int32) m(int32, int64) m(int64, int32) m(int64, int64) \
      m(uint32, int32) m(uint32, int64) m(uint64, int32) m(uint64, int64)

template <typename T, typename TIndices>
class EmbeddingBufferIndex : public ResourceBase {
 public:
  EmbeddingBufferIndex(const string& name, const int64 size)
#if HYBRIDBACKEND_SPARSEHASH
      : name_(name), size_(size), counter_(static_cast<TIndices>(0)) {
    map_.set_empty_key(std::numeric_limits<T>::max());
    map_.set_deleted_key(std::numeric_limits<T>::max() - 1);
    map_.reserve(size);
    debug_string_ = absl::StrCat("EmbeddingBufferIndex(name=", name_,
                                 ", size=", size_, ")");
  }
#else
      : name_(name), size_(size) {
  }
#endif

#if (TF_MAJOR_VERSION * 1000L + TF_MINOR_VERSION) >= 1015L
  string DebugString() const override { return debug_string_; }
#else
  string DebugString() override { return debug_string_; }
#endif

  int64 MemoryUsed() const override {
#if HYBRIDBACKEND_SPARSEHASH
    return static_cast<int64>(map_.size() * (sizeof(T) + sizeof(TIndices)));
#else
    return 0;
#endif
  }

  Status Lookup(const Tensor& values, Tensor* out_indices,
                TIndices* out_hit_size, Tensor* out_hit_rows,
                TIndices* out_miss_size, Tensor* out_miss_rows) {
#if HYBRIDBACKEND_SPARSEHASH
    const T* h_values = values.flat<T>().data();
    if (TF_PREDICT_FALSE(1 != values.shape().dims())) {
      return errors::InvalidArgument("Input to lookup must be 1-dimensional.");
    }

    TIndices size = static_cast<TIndices>(values.NumElements());
    if (TF_PREDICT_FALSE(size < static_cast<TIndices>(1))) {
      *out_hit_size = static_cast<TIndices>(0);
      *out_miss_size = static_cast<TIndices>(0);
      return Status::OK();
    }

    TIndices* h_out_indices = out_indices->flat<TIndices>().data();
    TIndices* h_out_hit_rows = out_hit_rows->flat<TIndices>().data();
    TIndices* h_out_miss_rows = out_miss_rows->flat<TIndices>().data();

    TIndices jmiss = 0;
    TIndices j = 0;
    for (TIndices i = 0; i < size; ++i) {
      const auto& v = h_values[i];
      auto it = map_.find(v);
      if (map_.end() == it) {
        h_out_miss_rows[jmiss] = i;
        auto c = counter_++;
        h_out_indices[i] = c;
        map_[v] = c;
        ++jmiss;
      } else {
        h_out_hit_rows[j] = i;
        h_out_indices[i] = it->second;
        ++j;
      }
    }

    *out_miss_size = jmiss;
    *out_hit_size = j;
#endif
    return Status::OK();
  }

  Status Dump(const int64 max_to_keep, Tensor* out_values,
              Tensor* out_indices) {
#if HYBRIDBACKEND_SPARSEHASH
    T* h_out_values = out_values->flat<T>().data();
    TIndices* h_out_indices = out_indices->flat<TIndices>().data();
    std::vector<T> to_be_deleted;
    T value;
    TIndices index;
    size_t j = 0;
    for (auto it = map_.begin(); it != map_.end(); ++it, ++j) {
      value = it->first;
      index = it->second;
      h_out_values[j] = value;
      h_out_indices[j] = index;
      if (index > max_to_keep) {
        to_be_deleted.push_back(value);
        --counter_;
      }
    }
    for (auto v : to_be_deleted) {
      map_.erase(v);
    }
#endif
    return Status::OK();
  }

  size_t size() const {
#if HYBRIDBACKEND_SPARSEHASH
    return map_.size();
#else
    return 0;
#endif
  }

  bool overflowed() const {
#if HYBRIDBACKEND_SPARSEHASH
    return counter_ > size_;
#else
    return false;
#endif
  }

 private:
  string debug_string_;
  string name_;
  int64 size_;
#if HYBRIDBACKEND_SPARSEHASH
  TIndices counter_;
  google::dense_hash_map<T, TIndices> map_;
#endif
  TF_DISALLOW_COPY_AND_ASSIGN(EmbeddingBufferIndex);
};

REGISTER_OP("HbEmbeddingBufferIndexHandleOp")
    .Output("resource: resource")
    .Attr("container: string = ''")
    .Attr("shared_name: string = ''")
    .Attr("dtype: {int32, int64, uint32, uint64}")
    .Attr("indices_dtype: {int32, int64}")
    .SetIsStateful()
    .SetShapeFn(tensorflow::shape_inference::ScalarShape)
    .Doc(R"doc(
Handle of a buffer index.

resource: Handle of a buffer index.
container: Container of the resource.
shared_name: Shared name of the resource.
dtype: Data type of inputs.
indices_dtype: Data type of indices.
)doc");

#define REGISTER_EMBEDDING_BUFFER_INDEX_HANDLE_KERNEL(Type, IndicesType) \
  REGISTER_KERNEL_BUILDER(                                               \
      Name("HbEmbeddingBufferIndexHandleOp")                             \
          .Device(DEVICE_CPU)                                            \
          .TypeConstraint<Type>("dtype")                                 \
          .TypeConstraint<IndicesType>("indices_dtype"),                 \
      ResourceHandleOp<EmbeddingBufferIndex<Type, IndicesType>>);
TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(
    REGISTER_EMBEDDING_BUFFER_INDEX_HANDLE_KERNEL);

REGISTER_OP("HbEmbeddingBufferIndexIsInitialized")
    .Output("is_initialized: bool")
    .Input("handle: resource")
    .Attr("dtype: {int32, int64, uint32, uint64}")
    .Attr("indices_dtype: {int32, int64}")
    .SetShapeFn(tensorflow::shape_inference::ScalarShape)
    .Doc(R"doc(
Checks whether a buffer index has been initialized.

is_initialized: True if the buffer index is initialized.
handle: Handle of a buffer index.
dtype: Data type of inputs.
indices_dtype: Data type of indices.
)doc");

#define REGISTER_EMBEDDING_BUFFER_INDEX_IS_INITIALIZED_KERNEL(Type,        \
                                                              IndicesType) \
  REGISTER_KERNEL_BUILDER(                                                 \
      Name("HbEmbeddingBufferIndexIsInitialized")                          \
          .Device(DEVICE_CPU)                                              \
          .TypeConstraint<Type>("dtype")                                   \
          .TypeConstraint<IndicesType>("indices_dtype"),                   \
      IsResourceInitialized<EmbeddingBufferIndex<Type, IndicesType>>);
TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(
    REGISTER_EMBEDDING_BUFFER_INDEX_IS_INITIALIZED_KERNEL);

#define REGISTER_EMBEDDING_BUFFER_INDEX_KERNEL(OpName, OpKernel, Type,       \
                                               IndicesType)                  \
  REGISTER_KERNEL_BUILDER(Name(OpName)                                       \
                              .Device(DEVICE_CPU)                            \
                              .TypeConstraint<Type>("dtype")                 \
                              .TypeConstraint<IndicesType>("indices_dtype"), \
                          OpKernel<Type, IndicesType>);

REGISTER_OP("HbEmbeddingBufferIndexCreate")
    .Input("handle: resource")
    .Attr("size: int")
    .Attr("shared_name: string")
    .Attr("dtype: {int32, int64, uint32, uint64}")
    .Attr("indices_dtype: {int32, int64}")
    .SetShapeFn(tensorflow::shape_inference::NoOutputs)
    .Doc(R"doc(
Creates a buffer index and returns a handle to it.

handle: Handle of a buffer index.
size: Size of a buffer index.
shared_name: Name of a buffer index.
dtype: Data type of inputs.
indices_dtype: Data type of indices.
)doc");

template <typename T, typename TIndices>
class EmbeddingBufferIndexCreateOp : public OpKernel {
 public:
  explicit EmbeddingBufferIndexCreateOp(OpKernelConstruction* ctx)
      : OpKernel(ctx) {
    OP_REQUIRES_OK(ctx, ctx->GetAttr("size", &size_));
    OP_REQUIRES_OK(ctx, ctx->GetAttr("shared_name", &name_));
  }

  void Compute(OpKernelContext* ctx) override {
    EmbeddingBufferIndex<T, TIndices>* buffer_index =
        new EmbeddingBufferIndex<T, TIndices>(name_, size_);
    Status s = CreateResource(ctx, HandleFromInput(ctx, 0), buffer_index);
    if (!s.ok() && s.code() != error::ALREADY_EXISTS) {
      OP_REQUIRES(ctx, false, s);
    }
  }

 private:
  int64 size_;
  string name_;
};

#define REGISTER_KERNEL(Type, IndicesType)                                   \
  REGISTER_EMBEDDING_BUFFER_INDEX_KERNEL("HbEmbeddingBufferIndexCreate",     \
                                         EmbeddingBufferIndexCreateOp, Type, \
                                         IndicesType);
TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(REGISTER_KERNEL);
#undef REGISTER_KERNEL

REGISTER_OP("HbEmbeddingBufferIndexLookup")
    .Output("out_indices: indices_dtype")
    .Output("out_hit_rows: indices_dtype")
    .Output("out_miss_rows: indices_dtype")
    .Input("handle: resource")
    .Input("values: dtype")
    .Attr("dtype: {int32, int64, uint32, uint64}")
    .Attr("indices_dtype: {int32, int64}")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      c->set_output(0, c->input(1));
      c->set_output(1, c->UnknownShape());
      c->set_output(2, c->UnknownShape());
      return Status::OK();
    })
    .SetIsStateful()
    .Doc(R"doc(
Looks up a buffer index.

out_indices: Indices of values.
out_hit_rows: Rows of hit values.
out_miss_rows: Rows of miss values.
handle: Handle of a buffer index.
dtype: Data type of inputs.
indices_dtype: Data type of indices.
)doc");

#if HYBRIDBACKEND_SPARSEHASH
template <typename T, typename TIndices>
class EmbeddingBufferIndexLookupOp : public OpKernel {
 public:
  explicit EmbeddingBufferIndexLookupOp(OpKernelConstruction* ctx)
      : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    EmbeddingBufferIndex<T, TIndices>* buffer_index;
    OP_REQUIRES_OK(ctx,
                   LookupResource(ctx, HandleFromInput(ctx, 0), &buffer_index));

    const Tensor& values = ctx->input(1);

    AllocatorAttributes host_alloc_attrs;
    host_alloc_attrs.set_on_host(true);
    host_alloc_attrs.set_gpu_compatible(true);

    Tensor* out_indices;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, values.shape(), &out_indices,
                                             host_alloc_attrs));

    Tensor* out_hit_rows = new Tensor();
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DataTypeToEnum<TIndices>::value, values.shape(),
                                out_hit_rows, host_alloc_attrs));

    Tensor* out_miss_rows = new Tensor();
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DataTypeToEnum<TIndices>::value, values.shape(),
                                out_miss_rows, host_alloc_attrs));

    TIndices hit_size = 0;
    TIndices miss_size = 0;
    OP_REQUIRES_OK(
        ctx, buffer_index->Lookup(values, out_indices, &hit_size, out_hit_rows,
                                  &miss_size, out_miss_rows));

    ctx->set_output(1, out_hit_rows->Slice(0, hit_size));
    ctx->set_output(2, out_miss_rows->Slice(0, miss_size));
  }
};

#define REGISTER_KERNEL(Type, IndicesType)                                   \
  REGISTER_EMBEDDING_BUFFER_INDEX_KERNEL("HbEmbeddingBufferIndexLookup",     \
                                         EmbeddingBufferIndexLookupOp, Type, \
                                         IndicesType);
TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(REGISTER_KERNEL);
#undef REGISTER_KERNEL
#endif

REGISTER_OP("HbEmbeddingBufferIndexDump")
    .Output("out_values: dtype")
    .Output("out_indices: indices_dtype")
    .Input("handle: resource")
    .Attr("max_to_keep: int")
    .Attr("dtype: {int32, int64, uint32, uint64}")
    .Attr("indices_dtype: {int32, int64}")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      c->set_output(0, c->UnknownShape());
      c->set_output(1, c->UnknownShape());
      return Status::OK();
    })
    .SetIsStateful()
    .Doc(R"doc(
Dumps a buffer index.

out_values: Values in the index.
out_indices: Indices in the index.
handle: Handle of a buffer index.
max_to_keep: Max items to keep after dump.
dtype: Data type of inputs.
indices_dtype: Data type of indices.
)doc");

#if HYBRIDBACKEND_SPARSEHASH
template <typename T, typename TIndices>
class EmbeddingBufferIndexDumpOp : public OpKernel {
 public:
  explicit EmbeddingBufferIndexDumpOp(OpKernelConstruction* ctx)
      : OpKernel(ctx) {
    OP_REQUIRES_OK(ctx, ctx->GetAttr("max_to_keep", &max_to_keep_));
  }

  void Compute(OpKernelContext* ctx) override {
    EmbeddingBufferIndex<T, TIndices>* buffer_index;
    OP_REQUIRES_OK(ctx,
                   LookupResource(ctx, HandleFromInput(ctx, 0), &buffer_index));

    TIndices size = buffer_index->size();

    Tensor* out_values = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {size}, &out_values));

    Tensor* out_indices = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(1, {size}, &out_indices));

    OP_REQUIRES_OK(ctx,
                   buffer_index->Dump(max_to_keep_, out_values, out_indices));
  }

 private:
  int64 max_to_keep_;
};

#define REGISTER_KERNEL(Type, IndicesType)                                 \
  REGISTER_EMBEDDING_BUFFER_INDEX_KERNEL("HbEmbeddingBufferIndexDump",     \
                                         EmbeddingBufferIndexDumpOp, Type, \
                                         IndicesType);
TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(REGISTER_KERNEL);
#undef REGISTER_KERNEL
#endif

REGISTER_OP("HbEmbeddingBufferIndexIsOverflowed")
    .Output("overflowed: bool")
    .Input("handle: resource")
    .Attr("dtype: {int32, int64, uint32, uint64}")
    .Attr("indices_dtype: {int32, int64}")
    .SetShapeFn(shape_inference::ScalarShape)
    .SetIsStateful()
    .Doc(R"doc(
Checks if a buffer index is overflowed.

overflowed: The index is overflowed or not.
handle: Handle of a buffer index.
dtype: Data type of inputs.
indices_dtype: Data type of indices.
)doc");

#if HYBRIDBACKEND_SPARSEHASH
template <typename T, typename TIndices>
class EmbeddingBufferIndexIsOverflowedOp : public OpKernel {
 public:
  explicit EmbeddingBufferIndexIsOverflowedOp(OpKernelConstruction* ctx)
      : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    EmbeddingBufferIndex<T, TIndices>* buffer_index;
    OP_REQUIRES_OK(ctx,
                   LookupResource(ctx, HandleFromInput(ctx, 0), &buffer_index));

    Tensor* is_overflowed = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {}, &is_overflowed));
    is_overflowed->scalar<bool>()() = buffer_index->overflowed();
  }
};

#define REGISTER_KERNEL(Type, IndicesType)                                     \
  REGISTER_EMBEDDING_BUFFER_INDEX_KERNEL("HbEmbeddingBufferIndexIsOverflowed", \
                                         EmbeddingBufferIndexIsOverflowedOp,   \
                                         Type, IndicesType);
TF_CALL_EMBEDDING_BUFFER_KEY_TYPES(REGISTER_KERNEL);
#undef REGISTER_KERNEL
#endif

}  // namespace hybridbackend
}  // namespace tensorflow
