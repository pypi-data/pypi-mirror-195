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
#include "hybridbackend/tensorflow/ops/sparse/segment/sum_functors.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"

namespace tensorflow {

namespace hybridbackend {

REGISTER_OP("HbSparseSegmentSumN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: realnumbertype")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentSumNOp : public OpKernel {
 public:
  SparseSegmentSumNOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    OpInputList data_list;
    OpInputList indices_list;
    OpInputList segment_ids_list;
    OpInputList num_segments_list;
    OpOutputList outputs;

    auto* range =
        ::hybridbackend::ProfilerRange::forLookup("SparseSegmentSumN");
    OP_REQUIRES_OK(ctx, ctx->input_list("data", &data_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("indices", &indices_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("segment_ids", &segment_ids_list));
    OP_REQUIRES_OK(ctx, ctx->output_list("outputs", &outputs));

    int32 num_columns = data_list.size();
    std::vector<int32> output_rows(num_columns);
    for (int i = 0; i < output_rows.size(); ++i) {
      output_rows[i] = -1;
    }

    for (int i = 0; i < num_columns; i++) {
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(indices_list[i].shape()),
                  errors::InvalidArgument("indices should be a vector."));
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(segment_ids_list[i].shape()),
                  errors::InvalidArgument("segment_ids should be a vector."));

      const int64 num_indices = indices_list[i].NumElements();
      OP_REQUIRES(ctx, num_indices == segment_ids_list[i].NumElements(),
                  errors::InvalidArgument(
                      "segment_ids and indices should have same size."));
    }

    typedef int32 OutputRow;
    std::vector<OutputRow> max_id(num_columns);
    std::vector<OutputRow> last_segment_id_plus_one(num_columns);
    for (int i = 0; i < num_columns; i++) {
      functor::FindMaxSegId<OutputRow> find_max_seg_functor_;
      find_max_seg_functor_(ctx, &segment_ids_list[i], max_id[i]);
      last_segment_id_plus_one[i] = max_id[i] + 1;

      output_rows[i] = last_segment_id_plus_one[i];

      OP_REQUIRES(ctx, output_rows[i] >= 0,
                  errors::InvalidArgument("segment ids must be >= 0"));
      TensorShape output_shape = data_list[i].shape();
      output_shape.set_dim(0, output_rows[i]);

      Tensor* output = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(i, output_shape, &output));
    }

    // set default value to output
    functor::SparseSegmentSumNFunctor<T, Tidx> impl;
    impl(ctx, &data_list, &indices_list, &segment_ids_list, &outputs);
    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }
};

#define REGISTER_SPARSE_SEGMENT_SUM_N(type, idx_type)            \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentSumN")            \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentSumNOp<type, idx_type, idx_type>);

#define REGISTER_SPARSE_SEGMENT_SUM_N_ALL(type) \
  REGISTER_SPARSE_SEGMENT_SUM_N(type, int32);   \
  REGISTER_SPARSE_SEGMENT_SUM_N(type, int64);
TF_CALL_SEGMENT_REDUCTION_TYPES(REGISTER_SPARSE_SEGMENT_SUM_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_SUM_N_ALL
#undef REGISTER_SPARSE_SEGMENT_SUM_N
#endif

REGISTER_OP("HbSparseSegmentSum1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: realnumbertype")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_SUM(type, idx_type)              \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentSum1")            \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentSumNOp<type, idx_type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_SUM_ALL(type) \
  REGISTER_SPARSE_SEGMENT_SUM(type, int32);   \
  REGISTER_SPARSE_SEGMENT_SUM(type, int64);
TF_CALL_SEGMENT_REDUCTION_TYPES(REGISTER_SPARSE_SEGMENT_SUM_ALL);
#undef REGISTER_SPARSE_SEGMENT_SUM_ALL
#undef REGISTER_SPARSE_SEGMENT_SUM
#endif

REGISTER_OP("HbSparseSegmentSumWithNumSegmentsN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: realnumbertype")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionWithNumSegmentsNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentSumWithNumSegmentsNOp : public OpKernel {
 public:
  SparseSegmentSumWithNumSegmentsNOp(OpKernelConstruction* ctx)
      : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    OpInputList data_list;
    OpInputList indices_list;
    OpInputList segment_ids_list;
    OpInputList num_segments_list;
    OpOutputList outputs;

    auto* range = ::hybridbackend::ProfilerRange::forLookup(
        "SparseSegmentSumWithNumSegmentsN");
    OP_REQUIRES_OK(ctx, ctx->input_list("data", &data_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("indices", &indices_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("segment_ids", &segment_ids_list));
    OP_REQUIRES_OK(ctx, ctx->output_list("outputs", &outputs));

    int32 num_columns = data_list.size();
    std::vector<int32> output_rows(num_columns);
    for (int i = 0; i < output_rows.size(); ++i) {
      output_rows[i] = -1;
    }

    OP_REQUIRES_OK(ctx, ctx->input_list("num_segments", &num_segments_list));
    for (int i = 0; i < num_columns; i++) {
      OP_REQUIRES(
          ctx, num_segments_list[i].shape().dims() == 0,
          errors::InvalidArgument("num_segments should be a scalar, not shape ",
                                  num_segments_list[i].shape().DebugString()));
      output_rows[i] = num_segments_list[i].scalar<int32>()();
      OP_REQUIRES(ctx, output_rows[i] >= 0,
                  errors::InvalidArgument("segment ids must be >= 0"));
    }

    for (int i = 0; i < num_columns; i++) {
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(indices_list[i].shape()),
                  errors::InvalidArgument("indices should be a vector."));
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(segment_ids_list[i].shape()),
                  errors::InvalidArgument("segment_ids should be a vector."));

      const int64 num_indices = indices_list[i].NumElements();
      OP_REQUIRES(ctx, num_indices == segment_ids_list[i].NumElements(),
                  errors::InvalidArgument(
                      "segment_ids and indices should have same size."));
    }

    typedef int32 OutputRow;
    std::vector<OutputRow> max_id(num_columns);
    std::vector<OutputRow> last_segment_id_plus_one(num_columns);
    for (int i = 0; i < num_columns; i++) {
      functor::FindMaxSegId<OutputRow> find_max_seg_functor_;
      find_max_seg_functor_(ctx, &segment_ids_list[i], max_id[i]);
      last_segment_id_plus_one[i] = max_id[i] + 1;

      OP_REQUIRES(
          ctx, output_rows[i] >= last_segment_id_plus_one[i],
          errors::InvalidArgument("segment ids must be < num_segments"));

      OP_REQUIRES(ctx, output_rows[i] >= 0,
                  errors::InvalidArgument("segment ids must be >= 0"));
      TensorShape output_shape = data_list[i].shape();
      output_shape.set_dim(0, output_rows[i]);

      Tensor* output = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(i, output_shape, &output));
    }

    // set default value to output
    functor::SparseSegmentSumNFunctor<T, Tidx> impl;
    impl(ctx, &data_list, &indices_list, &segment_ids_list, &outputs);
    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }
};

#define REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N(type, idx_type,   \
                                                        numsegments_type) \
  REGISTER_KERNEL_BUILDER(                                                \
      Name("HbSparseSegmentSumWithNumSegmentsN")                          \
          .Device(DEVICE_GPU)                                             \
          .HostMemory("num_segments")                                     \
          .TypeConstraint<type>("T")                                      \
          .TypeConstraint<numsegments_type>("Tnumsegments")               \
          .TypeConstraint<idx_type>("Tidx"),                              \
      SparseSegmentSumWithNumSegmentsNOp<type, idx_type, numsegments_type>);

#define REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N_ALL(type)      \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N(type, int32, int32); \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N(type, int32, int64); \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N(type, int64, int32); \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_TYPES(
    REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N_ALL
#undef REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_N
#endif

REGISTER_OP("HbSparseSegmentSumWithNumSegments1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: realnumbertype")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionWithNumSegmentsNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS(type, idx_type,   \
                                                      numsegments_type) \
  REGISTER_KERNEL_BUILDER(                                              \
      Name("HbSparseSegmentSumWithNumSegments1")                        \
          .Device(DEVICE_GPU)                                           \
          .HostMemory("num_segments")                                   \
          .TypeConstraint<type>("T")                                    \
          .TypeConstraint<numsegments_type>("Tnumsegments")             \
          .TypeConstraint<idx_type>("Tidx"),                            \
      SparseSegmentSumWithNumSegmentsNOp<type, idx_type, numsegments_type>);
#define REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_ALL(type)      \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS(type, int32, int32); \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS(type, int32, int64); \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS(type, int64, int32); \
  REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_TYPES(
    REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_ALL);
#undef REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS_ALL
#undef REGISTER_SPARSE_SEGMENT_SUM_WITH_NUM_SEGMENTS
#endif

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
