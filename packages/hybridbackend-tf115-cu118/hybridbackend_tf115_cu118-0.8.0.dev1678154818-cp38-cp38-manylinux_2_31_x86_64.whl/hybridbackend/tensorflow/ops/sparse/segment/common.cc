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
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/public/version.h>

#include "hybridbackend/tensorflow/ops/sparse/segment/common.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"

namespace tensorflow {
namespace hybridbackend {

Status SparseSegmentReductionNShapeFn(shape_inference::InferenceContext* c) {
  int32 num_columns;
  TF_RETURN_IF_ERROR(c->GetAttr("N", &num_columns));
  for (int i = 0; i < num_columns; ++i) {
    shape_inference::ShapeHandle data_shape;
    TF_RETURN_IF_ERROR(c->WithRankAtLeast(c->input(i), 1, &data_shape));

    shape_inference::ShapeHandle indices_shape;
    TF_RETURN_IF_ERROR(
        c->WithRank(c->input(i + num_columns), 1, &indices_shape));

    shape_inference::ShapeHandle segment_ids_shape;
    TF_RETURN_IF_ERROR(
        c->WithRank(c->input(i + 2 * num_columns), 1, &segment_ids_shape));

    shape_inference::ShapeHandle unused;
    TF_RETURN_IF_ERROR(c->Merge(indices_shape, segment_ids_shape, &unused));

    shape_inference::ShapeHandle subshape;
    TF_RETURN_IF_ERROR(c->Subshape(data_shape, 1, &subshape));

    shape_inference::ShapeHandle out;
    TF_RETURN_IF_ERROR(c->Concatenate(
        c->Vector(shape_inference::InferenceContext::kUnknownDim), subshape,
        &out));
    c->set_output(i, out);
  }
  // indices and segment_ids should merge cleanly.
  return Status::OK();
}

Status SparseSegmentReductionWithNumSegmentsNShapeFn(
    shape_inference::InferenceContext* c) {
  int32 num_columns;
  TF_RETURN_IF_ERROR(c->GetAttr("N", &num_columns));

  for (int i = 0; i < num_columns; ++i) {
    shape_inference::ShapeHandle data_shape;
    TF_RETURN_IF_ERROR(c->WithRankAtLeast(c->input(i), 1, &data_shape));

    shape_inference::ShapeHandle indices_shape;
    TF_RETURN_IF_ERROR(
        c->WithRank(c->input(i + num_columns), 1, &indices_shape));

    shape_inference::ShapeHandle segment_ids_shape;
    TF_RETURN_IF_ERROR(
        c->WithRank(c->input(i + 2 * num_columns), 1, &segment_ids_shape));

    shape_inference::ShapeHandle num_segments_shape;
    TF_RETURN_IF_ERROR(
        c->WithRank(c->input(i + 3 * num_columns), 0, &num_segments_shape));

    // indices and segment_ids should merge cleanly.
    shape_inference::ShapeHandle unused;
    TF_RETURN_IF_ERROR(c->Merge(indices_shape, segment_ids_shape, &unused));

    shape_inference::ShapeHandle subshape;
    TF_RETURN_IF_ERROR(c->Subshape(data_shape, 1, &subshape));

    shape_inference::ShapeHandle out;
    const Tensor* dim0 = c->input_tensor(i + 3 * num_columns);
    if (dim0 == nullptr) {
      // We don't have the value at inference time, so the output
      // shape is unknown.
      TF_RETURN_IF_ERROR(c->Concatenate(
          c->Vector(shape_inference::InferenceContext::kUnknownDim), subshape,
          &out));
    } else {
      auto dim0_value = dim0->scalar<int32>()();
      if (dim0_value < 0) {
        return errors::InvalidArgument(
            "Cannot specify a negative value for num_segments");
      }
      TF_RETURN_IF_ERROR(c->Concatenate(c->Vector(dim0_value), subshape, &out));
    }
    c->set_output(i, out);
  }
  return Status::OK();
}

Status SparseSegmentReductionGradNShapeFn(
    shape_inference::InferenceContext* c) {
  int32 num_columns;
  TF_RETURN_IF_ERROR(c->GetAttr("N", &num_columns));
  for (int i = 0; i < num_columns; ++i) {
    shape_inference::ShapeHandle data_shape;
    TF_RETURN_IF_ERROR(c->WithRankAtLeast(c->input(i), 1, &data_shape));

    shape_inference::ShapeHandle indices_shape;
    TF_RETURN_IF_ERROR(
        c->WithRank(c->input(i + num_columns), 1, &indices_shape));

    // indices and segment_ids should merge cleanly.
    shape_inference::ShapeHandle unused;
    TF_RETURN_IF_ERROR(
        c->Merge(c->input(i + 2 * num_columns), indices_shape, &unused));

    // output_dim0 should be a scalar
    TF_RETURN_IF_ERROR(c->WithRank(c->input(i + 3 * num_columns), 0, &unused));

    shape_inference::ShapeHandle subshape;
    TF_RETURN_IF_ERROR(c->Subshape(data_shape, 1, &subshape));

    const Tensor* dim0 = c->input_tensor(i + 3 * num_columns);
    shape_inference::ShapeHandle dim0_shape;
    if (dim0 == nullptr) {
      // We don't have the value at inference time, so the output
      // shape is unknown.
      dim0_shape = c->Vector(shape_inference::InferenceContext::kUnknownDim);
    } else {
      auto dim0_value = dim0->scalar<int32>()();
      if (dim0_value < 0) {
        return errors::InvalidArgument(
            "Cannot specify a negative value for output_dim0");
      }
      dim0_shape = c->Vector(dim0_value);
    }

    shape_inference::ShapeHandle out;
    TF_RETURN_IF_ERROR(c->Concatenate(dim0_shape, subshape, &out));
    c->set_output(i, out);
  }
  // indices and segment_ids should merge cleanly.
  return Status::OK();
}

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
