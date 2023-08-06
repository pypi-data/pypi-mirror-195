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
#include "hybridbackend/tensorflow/ops/sparse/segment/reduction_functors.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"

namespace tensorflow {

namespace hybridbackend {

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentReductionNOpBase : public OpKernel {
 public:
  SparseSegmentReductionNOpBase(const string& name, OpKernelConstruction* ctx,
                                bool has_num_segments, T default_value)
      : OpKernel(ctx),
        name_(name),
        has_num_segments_(has_num_segments),
        default_value_(default_value) {}

  void Compute(OpKernelContext* ctx) override {
    OpInputList data_list;
    OpInputList indices_list;
    OpInputList segment_ids_list;
    OpInputList num_segments_list;
    OpOutputList outputs;

    auto* range = ::hybridbackend::ProfilerRange::forLookup(name_);
    OP_REQUIRES_OK(ctx, ctx->input_list("data", &data_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("indices", &indices_list));
    OP_REQUIRES_OK(ctx, ctx->input_list("segment_ids", &segment_ids_list));
    OP_REQUIRES_OK(ctx, ctx->output_list("outputs", &outputs));

    int32 num_columns = data_list.size();
    std::vector<int32> output_rows(num_columns);
    for (int i = 0; i < output_rows.size(); ++i) {
      output_rows[i] = -1;
    }

    if (has_num_segments_) {
      OP_REQUIRES_OK(ctx, ctx->input_list("num_segments", &num_segments_list));
      for (int i = 0; i < num_columns; i++) {
        OP_REQUIRES(ctx, num_segments_list[i].shape().dims() == 0,
                    errors::InvalidArgument(
                        "num_segments should be a scalar, not shape ",
                        num_segments_list[i].shape().DebugString()));
        output_rows[i] = num_segments_list[i].scalar<int32>()();
        OP_REQUIRES(ctx, output_rows[i] >= 0,
                    errors::InvalidArgument("segment ids must be >= 0"));
      }
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

      if (has_num_segments_) {
        OP_REQUIRES(
            ctx, output_rows[i] >= last_segment_id_plus_one[i],
            errors::InvalidArgument("segment ids must be < num_segments"));
      } else {
        output_rows[i] = last_segment_id_plus_one[i];
      }
      OP_REQUIRES(ctx, output_rows[i] >= 0,
                  errors::InvalidArgument("segment ids must be >= 0"));
      TensorShape output_shape = data_list[i].shape();
      output_shape.set_dim(0, output_rows[i]);

      Tensor* output = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(i, output_shape, &output));
    }

    Reduce(ctx, &data_list, &indices_list, &segment_ids_list, &outputs);
    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }

  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) = 0;

 private:
  const string name_;
  const bool has_num_segments_;
  const T default_value_;
};
#endif

REGISTER_OP("HbSparseSegmentMeanN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentMeanNOp
    : public SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments> {
 public:
  SparseSegmentMeanNOp(OpKernelConstruction* ctx)
      : SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments>(
            "SparseSegmentMeanN", ctx, false /* has_num_segments */,
            T(0) /* default_value */) {}

  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) override {
    functor::SparseSegmentMeanNFunctor<T, Tidx> impl;
    impl(ctx, data_list, indices_list, segment_ids_list, outputs);
  }
};

#define REGISTER_SPARSE_SEGMENT_REDUCTION_N(type, idx_type)      \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentMeanN")           \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentMeanNOp<type, idx_type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_N_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_N(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_N(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(REGISTER_SPARSE_SEGMENT_REDUCTION_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_N_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_N
#endif

REGISTER_OP("HbSparseSegmentMean1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_REDUCTION_1(type, idx_type)      \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentMean1")           \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentMeanNOp<type, idx_type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_1_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_1(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_1(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(REGISTER_SPARSE_SEGMENT_REDUCTION_1_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_1_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_1
#endif

REGISTER_OP("HbSparseSegmentMeanWithNumSegmentsN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionWithNumSegmentsNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentMeanWithNumSegmentsNOp
    : public SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments> {
 public:
  SparseSegmentMeanWithNumSegmentsNOp(OpKernelConstruction* ctx)
      : SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments>(
            "SparseSegmentMeanWithNumSegmentsN", ctx,
            true /* has_num_segments */, T(0) /* default_value */) {}
  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) override {
    functor::SparseSegmentMeanNFunctor<T, Tidx> impl;
    impl(ctx, data_list, indices_list, segment_ids_list, outputs);
  }
};

#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N( \
    type, idx_type, numsegments_type)                          \
  REGISTER_KERNEL_BUILDER(                                     \
      Name("HbSparseSegmentMeanWithNumSegmentsN")              \
          .Device(DEVICE_GPU)                                  \
          .HostMemory("num_segments")                          \
          .TypeConstraint<type>("T")                           \
          .TypeConstraint<numsegments_type>("Tnumsegments")    \
          .TypeConstraint<idx_type>("Tidx"),                   \
      SparseSegmentMeanWithNumSegmentsNOp<type, idx_type, numsegments_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N_ALL(type)      \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int32, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int32, int64); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int64, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N
#endif

REGISTER_OP("HbSparseSegmentMeanWithNumSegments1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionWithNumSegmentsNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1( \
    type, idx_type, numsegments_type)                          \
  REGISTER_KERNEL_BUILDER(                                     \
      Name("HbSparseSegmentMeanWithNumSegments1")              \
          .Device(DEVICE_GPU)                                  \
          .HostMemory("num_segments")                          \
          .TypeConstraint<type>("T")                           \
          .TypeConstraint<numsegments_type>("Tnumsegments")    \
          .TypeConstraint<idx_type>("Tidx"),                   \
      SparseSegmentMeanWithNumSegmentsNOp<type, idx_type, numsegments_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1_ALL(type)      \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int32, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int32, int64); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int64, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1
#endif

REGISTER_OP("HbSparseSegmentSqrtNN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentSqrtNNOp
    : public SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments> {
 public:
  SparseSegmentSqrtNNOp(OpKernelConstruction* ctx)
      : SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments>(
            "SparseSegmentSqrtNN", ctx, false /* has_num_segments */,
            T(0) /* default_value */) {}
  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) override {
    functor::SparseSegmentSqrtNNFunctor<T, Tidx> impl;
    impl(ctx, data_list, indices_list, segment_ids_list, outputs);
  }
};

#define REGISTER_SPARSE_SEGMENT_REDUCTION_N(type, idx_type)      \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentSqrtNN")          \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentSqrtNNOp<type, idx_type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_N_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_N(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_N(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(REGISTER_SPARSE_SEGMENT_REDUCTION_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_N_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_N
#endif

REGISTER_OP("HbSparseSegmentSqrtN1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_REDUCTION_1(type, idx_type)      \
  REGISTER_KERNEL_BUILDER(Name("HbSparseSegmentSqrtN1")          \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<type>("T")         \
                              .TypeConstraint<idx_type>("Tidx"), \
                          SparseSegmentSqrtNNOp<type, idx_type, idx_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_1_ALL(type) \
  REGISTER_SPARSE_SEGMENT_REDUCTION_1(type, int32);   \
  REGISTER_SPARSE_SEGMENT_REDUCTION_1(type, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(REGISTER_SPARSE_SEGMENT_REDUCTION_1_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_1_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_1
#endif

REGISTER_OP("HbSparseSegmentSqrtNWithNumSegmentsN")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionWithNumSegmentsNShapeFn);

#if GOOGLE_CUDA
template <class T, typename Tidx, typename Tnumsegments>
class SparseSegmentSqrtNWithNumSegmentsNOp
    : public SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments> {
 public:
  SparseSegmentSqrtNWithNumSegmentsNOp(OpKernelConstruction* ctx)
      : SparseSegmentReductionNOpBase<T, Tidx, Tnumsegments>(
            "SparseSegmentSqrtNWithNumSegmentsN", ctx,
            true /* has_num_segments */, T(0) /* default_value */) {}
  virtual void Reduce(OpKernelContext* ctx, OpInputList* data_list,
                      OpInputList* indices_list, OpInputList* segment_ids_list,
                      OpOutputList* outputs) override {
    functor::SparseSegmentSqrtNNFunctor<T, Tidx> impl;
    impl(ctx, data_list, indices_list, segment_ids_list, outputs);
  }
};

#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N( \
    type, idx_type, numsegments_type)                          \
  REGISTER_KERNEL_BUILDER(                                     \
      Name("HbSparseSegmentSqrtNWithNumSegmentsN")             \
          .Device(DEVICE_GPU)                                  \
          .HostMemory("num_segments")                          \
          .TypeConstraint<type>("T")                           \
          .TypeConstraint<numsegments_type>("Tnumsegments")    \
          .TypeConstraint<idx_type>("Tidx"),                   \
      SparseSegmentSqrtNWithNumSegmentsNOp<type, idx_type, numsegments_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N_ALL(type)      \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int32, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int32, int64); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int64, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_N
#endif

REGISTER_OP("HbSparseSegmentSqrtNWithNumSegments1")
    .Output("outputs: N * T")
    .Input("data: N * T")
    .Input("indices: N * Tidx")
    .Input("segment_ids: N * int32")
    .Input("num_segments: N * Tnumsegments")
    .Attr("N: int >= 1")
    .Attr("T: {float, double}")
    .Attr("Tidx: {int32, int64} = DT_INT32")
    .Attr("Tnumsegments: {int32,int64} = DT_INT32")
    .SetShapeFn(SparseSegmentReductionWithNumSegmentsNShapeFn);
#if GOOGLE_CUDA
#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1( \
    type, idx_type, numsegments_type)                          \
  REGISTER_KERNEL_BUILDER(                                     \
      Name("HbSparseSegmentSqrtNWithNumSegments1")             \
          .Device(DEVICE_GPU)                                  \
          .HostMemory("num_segments")                          \
          .TypeConstraint<type>("T")                           \
          .TypeConstraint<numsegments_type>("Tnumsegments")    \
          .TypeConstraint<idx_type>("Tidx"),                   \
      SparseSegmentSqrtNWithNumSegmentsNOp<type, idx_type, numsegments_type>);
#define REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1_ALL(type)      \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int32, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int32, int64); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int64, int32); \
  REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1(type, int64, int64);
TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(
    REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1_ALL);
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1_ALL
#undef REGISTER_SPARSE_SEGMENT_REDUCTION_WITH_NUM_SEGMENTS_1
#endif

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
