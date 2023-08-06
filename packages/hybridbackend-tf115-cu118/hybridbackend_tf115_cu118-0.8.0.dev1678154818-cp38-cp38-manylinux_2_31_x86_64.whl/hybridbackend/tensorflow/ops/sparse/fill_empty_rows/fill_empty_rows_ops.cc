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
#if GOOGLE_CUDA
#define EIGEN_USE_GPU

#include <bitset>

#include <tensorflow/core/common_runtime/optimization_registry.h>
#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/register_types.h>
#include <tensorflow/core/framework/shape_inference.h>
#include <tensorflow/core/framework/tensor.pb.h>
#include <tensorflow/core/graph/node_builder.h>
#include <tensorflow/core/util/device_name_utils.h>

#include "hybridbackend/common/env.h"
#include "hybridbackend/common/profiler.h"
#include "hybridbackend/tensorflow/common/host_functions.h"
#include "hybridbackend/tensorflow/ops/sparse/fill_empty_rows/functors.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

REGISTER_OP("HbSparseFillEmptyRows")
    .Input("indices: int64")
    .Input("values: T")
    .Input("dense_shape: int64")
    .Input("default_value: T")
    .Output("output_indices: int64")
    .Output("output_values: T")
    .Output("empty_row_indicator: bool")
    .Output("reverse_index_map: int64")
    .Attr("T: type")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      shape_inference::ShapeHandle input_indices = c->input(0);
      TF_RETURN_IF_ERROR(c->WithRank(input_indices, 2, &input_indices));
      shape_inference::ShapeHandle input_values = c->input(1);
      TF_RETURN_IF_ERROR(c->WithRank(input_values, 1, &input_values));
      shape_inference::ShapeHandle input_shape = c->input(2);
      TF_RETURN_IF_ERROR(c->WithRank(input_shape, 1, &input_shape));
      shape_inference::ShapeHandle default_value = c->input(3);
      TF_RETURN_IF_ERROR(c->WithRank(default_value, 0, &default_value));
      shape_inference::DimensionHandle N = c->Dim(input_indices, 0);
      TF_RETURN_IF_ERROR(c->Merge(N, c->Dim(input_values, 0), &N));
      shape_inference::DimensionHandle unused_dim;
      TF_RETURN_IF_ERROR(c->Merge(c->Dim(input_indices, 1),
                                  c->Dim(input_shape, 0), &unused_dim));
      shape_inference::ShapeHandle output_indices =
          c->Matrix(shape_inference::InferenceContext::kUnknownDim,
                    c->NumElements(input_shape));
      shape_inference::ShapeHandle output_values =
          c->Vector(shape_inference::InferenceContext::kUnknownDim);
      shape_inference::ShapeHandle constant_input_shape;
      TF_RETURN_IF_ERROR(c->MakeShapeFromShapeTensor(2, &constant_input_shape));
      shape_inference::ShapeHandle empty_row_indicator =
          c->Vector(c->Dim(constant_input_shape, 0));
      shape_inference::ShapeHandle reverse_index_map = c->Vector(N);
      c->set_output(0, output_indices);
      c->set_output(1, output_values);
      c->set_output(2, empty_row_indicator);
      c->set_output(3, reverse_index_map);
      return Status::OK();
    });

template <typename T>
class SparseFillEmptyRowsOp : public OpKernel {
 public:
  explicit SparseFillEmptyRowsOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    const Tensor* indices_t;
    const Tensor* values_t;
    const Tensor* dense_shape_t;
    const Tensor* default_value_t;
    OP_REQUIRES_OK(ctx, ctx->input("indices", &indices_t));
    OP_REQUIRES_OK(ctx, ctx->input("values", &values_t));
    OP_REQUIRES_OK(ctx, ctx->input("dense_shape", &dense_shape_t));
    OP_REQUIRES_OK(ctx, ctx->input("default_value", &default_value_t));

    OP_REQUIRES(ctx, TensorShapeUtils::IsVector(dense_shape_t->shape()),
                errors::InvalidArgument("dense_shape must be a vector, saw: ",
                                        dense_shape_t->shape().DebugString()));
    OP_REQUIRES(ctx, TensorShapeUtils::IsMatrix(indices_t->shape()),
                errors::InvalidArgument("indices must be a matrix, saw: ",
                                        indices_t->shape().DebugString()));
    OP_REQUIRES(ctx, TensorShapeUtils::IsVector(values_t->shape()),
                errors::InvalidArgument("values must be a vector, saw: ",
                                        values_t->shape().DebugString()));
    OP_REQUIRES(
        ctx, TensorShapeUtils::IsScalar(default_value_t->shape()),
        errors::InvalidArgument("default_value must be a scalar, saw: ",
                                default_value_t->shape().DebugString()));

    const int64 dense_rows = dense_shape_t->vec<int64>()(0);
    const int64 N = indices_t->shape().dim_size(0);
    int rank = indices_t->shape().dim_size(1);

    Tensor* empty_row_indicator_t;
    OP_REQUIRES_OK(ctx,
                   ctx->allocate_output("empty_row_indicator", {dense_rows},
                                        &empty_row_indicator_t));

    Tensor* reverse_index_map_t;
    OP_REQUIRES_OK(ctx, ctx->allocate_output("reverse_index_map", {N},
                                             &reverse_index_map_t));

    if (TF_PREDICT_FALSE(dense_rows == 0)) {
      OP_REQUIRES(
          ctx, N == 0,
          errors::InvalidArgument("Received SparseTensor with dense_shape[0] = "
                                  "0 but indices.shape[0] = ",
                                  N));
      Tensor* output_indices_t;
      OP_REQUIRES_OK(ctx, ctx->allocate_output("output_indices", {0, rank},
                                               &output_indices_t));
      Tensor* output_values_t;
      OP_REQUIRES_OK(
          ctx, ctx->allocate_output("output_values", {0}, &output_values_t));

      return;
    }

    auto* range =
        ::hybridbackend::ProfilerRange::forLookup("SparseFillEmptyRows");

    const int64* d_indices = indices_t->flat<int64>().data();

    const T* d_values = values_t->flat<T>().data();

    const T default_value = default_value_t->scalar<T>()();

    bool* d_empty_row_indicator = empty_row_indicator_t->flat<bool>().data();

    int64* d_reverse_index_map = reverse_index_map_t->flat<int64>().data();

    Tensor scratch_t;
    OP_REQUIRES_OK(ctx,
                   ctx->allocate_temp(DT_INT64, TensorShape({dense_rows + 1}),
                                      &scratch_t));
    int64* d_empty_row_indices = scratch_t.flat<int64>().data();
    int64* d_num_empty_rows = scratch_t.flat<int64>().data() + dense_rows;
    se::DeviceMemoryBase num_empty_rows_ptr(d_num_empty_rows, sizeof(int64));

    functor::SparseFillEmptyRowsFunctors<T> functors(
        dense_rows, N, rank, default_value, d_indices, d_values,
        d_empty_row_indicator, d_reverse_index_map);

    functors.build_empty_row_indices(d_empty_row_indices, d_num_empty_rows,
                                     ctx->eigen_device<GPUDevice>());

    int64 num_empty_rows;
    ctx->op_device_context()->stream()->ThenMemcpy(
        &num_empty_rows, num_empty_rows_ptr, sizeof(int64));
    ctx->op_device_context()->stream()->BlockHostUntilDone();

    if (num_empty_rows > 0) {
      Tensor* output_indices_t;
      TensorShape output_indices_shape({N + num_empty_rows, rank});
      OP_REQUIRES_OK(
          ctx, ctx->allocate_output("output_indices", output_indices_shape,
                                    &output_indices_t));
      int64* d_output_indices = output_indices_t->flat<int64>().data();

      Tensor* output_values_t;
      OP_REQUIRES_OK(ctx,
                     ctx->allocate_output("output_values",
                                          TensorShape({N + num_empty_rows}),
                                          &output_values_t));
      T* d_output_values = output_values_t->flat<T>().data();

      se::DeviceMemoryBase output_indices_ptr(
          d_output_indices, (N + num_empty_rows) * rank * sizeof(int64));
      se::DeviceMemoryBase indices_ptr(const_cast<int64*>(d_indices),
                                       N * rank * sizeof(int64));
      ctx->op_device_context()->stream()->ThenMemcpy(
          &output_indices_ptr, indices_ptr, N * rank * sizeof(int64));

      se::DeviceMemoryBase output_values_ptr(
          d_output_values, (N + num_empty_rows) * rank * sizeof(T));
      se::DeviceMemoryBase values_ptr(const_cast<T*>(d_values), N * sizeof(T));
      ctx->op_device_context()->stream()->ThenMemcpy(&output_values_ptr,
                                                     values_ptr, N * sizeof(T));

      se::DeviceMemoryBase empty_indices_ptr(
          d_output_indices + N * rank, num_empty_rows * rank * sizeof(int64));
      ctx->op_device_context()->stream()->ThenMemset32(
          &empty_indices_ptr, 0, num_empty_rows * rank * sizeof(int64));
      functors.build_empty_rows(num_empty_rows, d_empty_row_indices,
                                d_output_indices, d_output_values,
                                ctx->eigen_device<GPUDevice>());
    } else {
      if (IsRefType(ctx->input_dtype(0))) {
        ctx->forward_ref_input_to_ref_output(0, 0);
      } else {
        ctx->set_output(0, ctx->input(0));
      }
      if (IsRefType(ctx->input_dtype(1))) {
        ctx->forward_ref_input_to_ref_output(1, 1);
      } else {
        ctx->set_output(1, ctx->input(1));
      }
    }

    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }
};

#define REGISTER_SPARSE_FILL_EMPTY_ROWS_KERNELS(TYPE)      \
  REGISTER_KERNEL_BUILDER(Name("HbSparseFillEmptyRows")    \
                              .Device(DEVICE_GPU)          \
                              .HostMemory("dense_shape")   \
                              .HostMemory("default_value") \
                              .TypeConstraint<TYPE>("T"),  \
                          SparseFillEmptyRowsOp<TYPE>)

TF_CALL_SPARSE_FILL_EMPTY_ROWS_TYPES(REGISTER_SPARSE_FILL_EMPTY_ROWS_KERNELS);
#undef REGISTER_SPARSE_FILL_EMPTY_ROWS_KERNELS

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
