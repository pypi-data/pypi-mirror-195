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

#if HYBRIDBACKEND_TENSORFLOW

#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/register_types.h>
#include <tensorflow/core/framework/shape_inference.h>

#include "hybridbackend/tensorflow/ops/sparse/count_nonzero/functors.h"

namespace tensorflow {
namespace hybridbackend {

REGISTER_OP("HbSparseCountNonzero")
    .Input("input_indices: Tidx")
    .Input("input_values: T")
    .Input("input_shape: int64")
    .Output("output: Tout")
    .Attr("axis: int = -1")
    .Attr("T: realnumbertype")
    .Attr("Tidx: {int32, int64}")
    .Attr("Tout: {int32, int64}")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      const Tensor* shape_tensor = c->input_tensor(2);
      int64 axis;
      TF_RETURN_IF_ERROR(c->GetAttr("axis", &axis));
      if (shape_tensor != nullptr) {
        auto shape_vec = shape_tensor->flat<int64>();
        int64 ndims = shape_vec.size();
        if (axis < 0) {
          axis = ndims + axis;
        }
        std::vector<shape_inference::DimensionHandle> dims;
        for (int d = 0; d < ndims; ++d) {
          if (d < axis) {
            dims.push_back(c->MakeDim(shape_vec(d)));
          }
        }
        c->set_output(0, c->MakeShape(dims));
      } else {
        c->set_output(0, c->UnknownShape());
      }
      return Status::OK();
    })
    .Doc(R"doc(
)doc");

REGISTER_OP("HbSparseCountNonzeroN")
    .Output("outputs: N * Tout")
    .Input("input_indices: N * Tidx")
    .Input("input_values: N * T")
    .Input("input_shapes: N * int64")
    .Attr("N: int >= 1")
    .Attr("axis: int = -1")
    .Attr("T: realnumbertype")
    .Attr("Tidx: {int32, int64}")
    .Attr("Tout: {int32, int64}")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      int32 num_columns;
      TF_RETURN_IF_ERROR(c->GetAttr("N", &num_columns));
      int64 axis;
      TF_RETURN_IF_ERROR(c->GetAttr("axis", &axis));
      for (int i = 0; i < num_columns; ++i) {
        const Tensor* shape_tensor = c->input_tensor(i + 2 * num_columns);
        if (shape_tensor != nullptr) {
          auto shape_vec = shape_tensor->flat<int64>();
          int64 ndims = shape_vec.size();
          if (axis < 0) {
            axis = ndims + axis;
          }
          std::vector<shape_inference::DimensionHandle> dims;
          for (int d = 0; d < ndims; ++d) {
            if (d < axis) {
              dims.push_back(c->MakeDim(shape_vec(d)));
            }
          }
          c->set_output(i, c->MakeShape(dims));
        } else {
          c->set_output(i, c->UnknownShape());
        }
      }
      return Status::OK();
    })
    .Doc(R"doc(
)doc");

#if GOOGLE_CUDA

using GPUDevice = Eigen::GpuDevice;
template <typename T, typename Tidx, typename Tout>
class SparseCountNonzeroOp : public OpKernel {
 public:
  explicit SparseCountNonzeroOp(OpKernelConstruction* ctx) : OpKernel(ctx) {
    OP_REQUIRES_OK(ctx, ctx->GetAttr("axis", &axis_));
  }

  void Compute(OpKernelContext* ctx) override {
    const Tensor& indices_t = ctx->input(0);
    const Tensor& values_t = ctx->input(1);
    // make shape for output
    const Tensor& shape_t = ctx->input(2);
    auto shape_vec = shape_t.flat<int64>();
    int64 ndims = shape_vec.size();
    if (axis_ < 0) {
      axis_ = ndims + axis_;
    }
    OP_REQUIRES(ctx, (axis_ > 0 && axis_ < ndims),
                errors::InvalidArgument("axis must be among (0, ndims)"));
    std::vector<int64> dims;
    for (int d = 0; d < ndims; ++d) {
      if (d < axis_) {
        dims.push_back(shape_vec(d));
      }
    }
    TensorShape output_shape = TensorShape(dims);
    Tensor* out_values = nullptr;
    // allocate output on GPU
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, output_shape, &out_values));
    // invoke the functor
    functor::SparseCountNonzeroFunctor<T, Tidx, Tout> count_functor_;
    count_functor_(ctx, &indices_t, &values_t, &shape_t, out_values, axis_,
                   ndims);
  }

 private:
  int64 axis_;
};

#define REGISTER_SPARSE_COUNT_NONZERO_KERNEL(T, Tidx, Tout)  \
  REGISTER_KERNEL_BUILDER(Name("HbSparseCountNonzero")       \
                              .Device(DEVICE_GPU)            \
                              .HostMemory("input_shape")     \
                              .TypeConstraint<T>("T")        \
                              .TypeConstraint<Tidx>("Tidx")  \
                              .TypeConstraint<Tout>("Tout"), \
                          SparseCountNonzeroOp<T, Tidx, Tout>)

#define REGISTER_SPARSE_COUNT_NONZERO_KERNEL_TYPE(T)     \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL(T, int32, int32); \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL(T, int64, int32); \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL(T, int32, int64); \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL(T, int64, int64);

TF_CALL_REAL_NUMBER_TYPES(REGISTER_SPARSE_COUNT_NONZERO_KERNEL_TYPE);

#undef REGISTER_SPARSE_COUNT_NONZERO_KERNEL_TYPE
#undef REGISTER_SPARSE_COUNT_NONZERO_KERNEL

template <typename T, typename Tidx, typename Tout>
class SparseCountNonzeroNOp : public OpKernel {
 public:
  explicit SparseCountNonzeroNOp(OpKernelConstruction* ctx) : OpKernel(ctx) {
    OP_REQUIRES_OK(ctx, ctx->GetAttr("axis", &axis_));
  }

  void Compute(OpKernelContext* ctx) override {
    OpInputList indices_list;
    OpInputList values_list;
    OpInputList shapes_list;
    OpOutputList outputs;

    OP_REQUIRES_OK(ctx, ctx->input_list("input_indices", &indices_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("input_values", &values_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("input_shapes", &shapes_list));
    OP_REQUIRES_OK(ctx, ctx->output_list("outputs", &outputs));

    int32 num_columns = indices_list.size();
    std::vector<int64> ndims_list;
    std::vector<int64> axis_list;
    for (int i = 0; i < num_columns; i++) {
      auto shape_vec = shapes_list[i].flat<int64>();
      int64 ndims = shape_vec.size();
      int64 axis_i = (axis_ < 0) ? ndims + axis_ : axis_;

      OP_REQUIRES(ctx, (axis_i > 0 && axis_i < ndims),
                  errors::InvalidArgument("axis must be among (0, ndims)"));
      std::vector<int64> dims;
      for (int d = 0; d < ndims; ++d) {
        if (d < axis_i) {
          dims.push_back(shape_vec(d));
        }
      }
      TensorShape output_shape = TensorShape(dims);
      Tensor* out_values = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(i, output_shape, &out_values));
      ndims_list.emplace_back(ndims);
      axis_list.emplace_back(axis_i);
    }

    functor::SparseCountNonzeroNFunctor<T, Tidx, Tout> count_functor_;
    count_functor_(ctx, &indices_list, &values_list, &shapes_list, &outputs,
                   axis_list, ndims_list);
  }

 private:
  int64 axis_;
};

#define REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N(T, Tidx, Tout) \
  REGISTER_KERNEL_BUILDER(Name("HbSparseCountNonzeroN")       \
                              .Device(DEVICE_GPU)             \
                              .HostMemory("input_shapes")     \
                              .TypeConstraint<T>("T")         \
                              .TypeConstraint<Tidx>("Tidx")   \
                              .TypeConstraint<Tout>("Tout"),  \
                          SparseCountNonzeroNOp<T, Tidx, Tout>)

#define REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N_TYPE(T)     \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N(T, int32, int32); \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N(T, int64, int32); \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N(T, int32, int64); \
  REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N(T, int64, int64);

TF_CALL_REAL_NUMBER_TYPES(REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N_TYPE);

#undef REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N_TYPE
#undef REGISTER_SPARSE_COUNT_NONZERO_KERNEL_N
#endif
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
