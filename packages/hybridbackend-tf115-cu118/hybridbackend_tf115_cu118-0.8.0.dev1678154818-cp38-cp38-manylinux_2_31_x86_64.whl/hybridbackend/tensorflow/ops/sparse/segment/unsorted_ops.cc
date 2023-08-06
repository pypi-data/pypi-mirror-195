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
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/unsorted_functors.h"

namespace tensorflow {
namespace hybridbackend {
Status UnsortedSegmentReductionNShapeFn(shape_inference::InferenceContext* c) {
  int32 num_columns;
  TF_RETURN_IF_ERROR(c->GetAttr("N", &num_columns));
  for (int i = 0; i < num_columns; ++i) {
    shape_inference::ShapeHandle s_data = c->input(i);
    shape_inference::ShapeHandle s_segment_ids = c->input(i + num_columns);
    shape_inference::ShapeHandle s_num_segments = c->input(i + 2 * num_columns);
    TF_RETURN_IF_ERROR(c->WithRank(s_num_segments, 0, &s_num_segments));
    shape_inference::ShapeHandle out;
    if (c->RankKnown(s_segment_ids)) {
      TF_RETURN_IF_ERROR(
          c->MergePrefix(s_data, s_segment_ids, &s_data, &s_segment_ids));

      // Get the value of the num_segments input tensor.
      shape_inference::DimensionHandle num_segments_dim;
      TF_RETURN_IF_ERROR(
          c->MakeDimForScalarInput(i + 2 * num_columns, &num_segments_dim));

      // Output is {segment_id_rank} + s_data[segment_id_rank:].
      shape_inference::ShapeHandle s_data_suffix;
      TF_RETURN_IF_ERROR(
          c->Subshape(s_data, c->Rank(s_segment_ids), &s_data_suffix));
      TF_RETURN_IF_ERROR(
          c->Concatenate(c->Vector(num_segments_dim), s_data_suffix, &out));
    } else {
      out = c->UnknownShape();
    }
    c->set_output(i, out);
  }
  return Status::OK();
}

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class UnsortedSegmentReductionNOpBase : public OpKernel {
 public:
  UnsortedSegmentReductionNOpBase(const string& name, OpKernelConstruction* ctx,
                                  T default_value)
      : OpKernel(ctx), name_(name), default_value_(default_value) {}

  void Compute(OpKernelContext* ctx) override {
    OpInputList data_list;
    OpInputList segment_ids_list;
    OpInputList num_segments_list;
    OpOutputList outputs;

    auto* range = ::hybridbackend::ProfilerRange::forLookup(name_);
    OP_REQUIRES_OK(ctx, ctx->input_list("data", &data_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("segment_ids", &segment_ids_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("num_segments", &num_segments_list));
    OP_REQUIRES_OK(ctx, ctx->output_list("outputs", &outputs));

    int32 num_columns = data_list.size();
    std::vector<int32> output_rows(num_columns);
    for (int i = 0; i < output_rows.size(); ++i) {
      output_rows[i] = -1;
    }

    for (int i = 0; i < num_columns; i++) {
      OP_REQUIRES(
          ctx, num_segments_list[i].shape().dims() == 0,
          errors::InvalidArgument("num_segments should be a scalar, not shape ",
                                  num_segments_list[i].shape().DebugString()));
      output_rows[i] = num_segments_list[i].scalar<Tidx>()();
      OP_REQUIRES(ctx, output_rows[i] >= 0,
                  errors::InvalidArgument("segment ids must be >= 0"));
      TensorShape output_shape = data_list[i].shape();
      output_shape.set_dim(0, output_rows[i]);
      Tensor* output = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(i, output_shape, &output));
    }

    for (int i = 0; i < num_columns; i++) {
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(segment_ids_list[i].shape()),
                  errors::InvalidArgument("segment_ids should be a vector."));
    }
    // set default value to output
    functor::UnsortedSegmentReductionNFunctor<T, Tidx> impl;
    impl(ctx, &data_list, &segment_ids_list, &outputs);
    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }

 private:
  const string name_;
  const T default_value_;
};
#endif

REGISTER_OP("HbUnsortedSegmentSumN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("segment_ids: N * Tindices")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: numbertype")
    .Attr("Tindices: {int32,int64}")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(UnsortedSegmentReductionNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class UnsortedSegmentSumNOp
    : public UnsortedSegmentReductionNOpBase<T, Tidx, Tnumsegments> {
 public:
  UnsortedSegmentSumNOp(OpKernelConstruction* ctx)
      : UnsortedSegmentReductionNOpBase<T, Tidx, Tnumsegments>(
            "UnsortedSegmentSumN", ctx, T(0)) {}
};

#define REGISTER_UNSORTED_SEGMENT_REDUCTION_N(type, idx_type,   \
                                              numsegments_type) \
  REGISTER_KERNEL_BUILDER(                                      \
      Name("HbUnsortedSegmentSumN")                             \
          .Device(DEVICE_GPU)                                   \
          .HostMemory("num_segments")                           \
          .TypeConstraint<type>("T")                            \
          .TypeConstraint<numsegments_type>("Tnumsegments")     \
          .TypeConstraint<idx_type>("Tindices"),                \
      UnsortedSegmentSumNOp<type, idx_type, numsegments_type>);

#define REGISTER_UNSORTED_SEGMENT_REDUCTION_N_ALL(type)      \
  REGISTER_UNSORTED_SEGMENT_REDUCTION_N(type, int32, int32); \
  REGISTER_UNSORTED_SEGMENT_REDUCTION_N(type, int32, int64); \
  REGISTER_UNSORTED_SEGMENT_REDUCTION_N(type, int64, int32); \
  REGISTER_UNSORTED_SEGMENT_REDUCTION_N(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_TYPES(REGISTER_UNSORTED_SEGMENT_REDUCTION_N_ALL);
#undef REGISTER_UNSORTED_SEGMENT_REDUCTION_N_ALL
#undef REGISTER_UNSORTED_SEGMENT_REDUCTION_N
#endif

REGISTER_OP("HbUnsortedSegmentSum1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("segment_ids: N * Tindices")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: numbertype")
    .Attr("Tindices: {int32,int64}")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(UnsortedSegmentReductionNShapeFn);

#if GOOGLE_CUDA
#define REGISTER_UNSORTED_SEGMENT_REDUCTION(type, idx_type, numsegments_type) \
  REGISTER_KERNEL_BUILDER(                                                    \
      Name("HbUnsortedSegmentSum1")                                           \
          .Device(DEVICE_GPU)                                                 \
          .HostMemory("num_segments")                                         \
          .TypeConstraint<type>("T")                                          \
          .TypeConstraint<numsegments_type>("Tnumsegments")                   \
          .TypeConstraint<idx_type>("Tindices"),                              \
      UnsortedSegmentSumNOp<type, idx_type, numsegments_type>);
#define REGISTER_UNSORTED_SEGMENT_REDUCTION_ALL(type)      \
  REGISTER_UNSORTED_SEGMENT_REDUCTION(type, int32, int32); \
  REGISTER_UNSORTED_SEGMENT_REDUCTION(type, int32, int64); \
  REGISTER_UNSORTED_SEGMENT_REDUCTION(type, int64, int32); \
  REGISTER_UNSORTED_SEGMENT_REDUCTION(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_TYPES(REGISTER_UNSORTED_SEGMENT_REDUCTION_ALL);
#undef REGISTER_UNSORTED_SEGMENT_REDUCTION_ALL
#undef REGISTER_UNSORTED_SEGMENT_REDUCTION
#endif

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
