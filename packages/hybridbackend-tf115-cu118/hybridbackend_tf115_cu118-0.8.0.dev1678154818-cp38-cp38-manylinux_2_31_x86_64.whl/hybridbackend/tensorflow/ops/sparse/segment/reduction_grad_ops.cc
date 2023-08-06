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

#include "hybridbackend/common/profiler.h"
#include "hybridbackend/tensorflow/common/host_functions.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/common.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/reduction_grad_functors.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"

namespace tensorflow {

namespace hybridbackend {

#if GOOGLE_CUDA
template <class T, typename Tidx>
class SparseSegmentReductionNGradOpBase : public OpKernel {
 public:
  SparseSegmentReductionNGradOpBase(const string& name,
                                    OpKernelConstruction* ctx)
      : OpKernel(ctx), name_(name) {}

  void Compute(OpKernelContext* ctx) override {
    OpInputList data_list;
    OpInputList indices_list;
    OpInputList segment_ids_list;
    OpInputList output_dim0_list;
    OpOutputList outputs;

    auto* range = ::hybridbackend::ProfilerRange::forLookup(name_);
    OP_REQUIRES_OK(ctx, ctx->input_list("grads", &data_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("indices", &indices_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("segment_ids", &segment_ids_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("output_dim0", &output_dim0_list));
    OP_REQUIRES_OK(ctx, ctx->output_list("outputs", &outputs));

    int32 num_columns = data_list.size();
    for (int i = 0; i < num_columns; i++) {
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(indices_list[i].shape()),
                  errors::InvalidArgument("indices should be a vector."));
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(segment_ids_list[i].shape()),
                  errors::InvalidArgument("segment_ids should be a vector."));
      OP_REQUIRES(
          ctx, output_dim0_list[i].shape().dims() == 0,
          errors::InvalidArgument("output_dim0 should be a scalar, not shape ",
                                  output_dim0_list[i].shape().DebugString()));
      const int64 num_indices = indices_list[i].NumElements();
      OP_REQUIRES(ctx, num_indices == segment_ids_list[i].NumElements(),
                  errors::InvalidArgument(
                      "segment_ids and indices should have same size."));
    }

    typedef int32 SegmentId;
    for (int i = 0; i < num_columns; i++) {
      SegmentId output_row = output_dim0_list[i].scalar<SegmentId>()();
      OP_REQUIRES(ctx, output_row >= 0,
                  errors::InvalidArgument("output row must be >= 0"));
      TensorShape output_shape = data_list[i].shape();
      output_shape.set_dim(0, output_row);
      Tensor* output = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(i, output_shape, &output));
    }
    this->Reduce(ctx, &data_list, &indices_list, &segment_ids_list, &outputs);
    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }

  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) = 0;

 private:
  const string name_;
};
#endif

REGISTER_OP("HbSparseSegmentMeanGradN")
    .Output("outputs: N * T")
    .Input("grads: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("output_dim0: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionGradNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx>
class SparseSegmentMeanGradNOp
    : public SparseSegmentReductionNGradOpBase<T, Tidx> {
 public:
  explicit SparseSegmentMeanGradNOp(OpKernelConstruction* ctx)
      : SparseSegmentReductionNGradOpBase<T, Tidx>("SparseSegmentMeanGradN",
                                                   ctx) {}
  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) override {
    functor::SparseSegmentMeanGradNFunctor<T, Tidx> impl;
    impl(ctx, data_list, indices_list, segment_ids_list, outputs);
  }
};

#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N(type, idx_type) \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentMeanGradN")       \
                              .Device(DEVICE_GPU)                \
                              .HostMemory("output_dim0")         \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentMeanGradNOp<type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N
#endif

REGISTER_OP("HbSparseSegmentMeanGrad1")
    .Output("outputs: N * T")
    .Input("grads: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("output_dim0: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionGradNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1(type, idx_type) \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentMeanGrad1")       \
                              .Device(DEVICE_GPU)                \
                              .HostMemory("output_dim0")         \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentMeanGradNOp<type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1
#endif

REGISTER_OP("HbSparseSegmentSqrtNGradN")
    .Output("outputs: N * T")
    .Input("grads: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("output_dim0: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionGradNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx>
class SparseSegmentSqrtNGradNOp
    : public SparseSegmentReductionNGradOpBase<T, Tidx> {
 public:
  explicit SparseSegmentSqrtNGradNOp(OpKernelConstruction* ctx)
      : SparseSegmentReductionNGradOpBase<T, Tidx>("SparseSegmentSqrtNGradN",
                                                   ctx) {}
  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) override {
    functor::SparseSegmentSqrtNGradNFunctor<T, Tidx> impl;
    impl(ctx, data_list, indices_list, segment_ids_list, outputs);
  }
};

#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N(type, idx_type) \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentSqrtNGradN")      \
                              .Device(DEVICE_GPU)                \
                              .HostMemory("output_dim0")         \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentSqrtNGradNOp<type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_N
#endif

REGISTER_OP("HbSparseSegmentSqrtNGrad1")
    .Output("outputs: N * T")
    .Input("grads: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("output_dim0: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionGradNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1(type, idx_type) \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentSqrtNGrad1")      \
                              .Device(DEVICE_GPU)                \
                              .HostMemory("output_dim0")         \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentSqrtNGradNOp<type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_GRAD_1
#endif

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
