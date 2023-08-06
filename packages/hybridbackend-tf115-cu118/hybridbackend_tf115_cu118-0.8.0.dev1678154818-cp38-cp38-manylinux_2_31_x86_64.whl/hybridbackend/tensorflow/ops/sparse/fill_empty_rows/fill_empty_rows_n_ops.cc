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

REGISTER_OP("HbSparseFillEmptyRowsN")
    .Input("indices: N * int64")
    .Input("values: N * T")
    .Input("dense_shape: N * int64")
    .Input("default_value: N * T")
    .Output("output_indices: N * int64")
    .Output("output_values: N * T")
    .Output("empty_row_indicator: N * bool")
    .Output("reverse_index_map: N * int64")
    .Attr("N: int >= 1")
    .Attr("T: type")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      int32 num_inputs;
      TF_RETURN_IF_ERROR(c->GetAttr("N", &num_inputs));
      for (int i = 0; i < num_inputs; ++i) {
        shape_inference::ShapeHandle input_indices = c->input(i);
        TF_RETURN_IF_ERROR(c->WithRank(input_indices, 2, &input_indices));
        shape_inference::ShapeHandle input_values = c->input(i + num_inputs);
        TF_RETURN_IF_ERROR(c->WithRank(input_values, 1, &input_values));
        shape_inference::ShapeHandle input_shape = c->input(i + 2 * num_inputs);
        TF_RETURN_IF_ERROR(c->WithRank(input_shape, 1, &input_shape));
        shape_inference::ShapeHandle default_value =
            c->input(i + 3 * num_inputs);
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
        TF_RETURN_IF_ERROR(c->MakeShapeFromShapeTensor(i + 2 * num_inputs,
                                                       &constant_input_shape));
        shape_inference::ShapeHandle empty_row_indicator =
            c->Vector(c->Dim(constant_input_shape, 0));
        shape_inference::ShapeHandle reverse_index_map = c->Vector(N);
        c->set_output(i, output_indices);
        c->set_output(i + num_inputs, output_values);
        c->set_output(i + 2 * num_inputs, empty_row_indicator);
        c->set_output(i + 3 * num_inputs, reverse_index_map);
      }
      return Status::OK();
    });

template <typename T>
class SparseFillEmptyRowsNOp : public OpKernel {
 public:
  explicit SparseFillEmptyRowsNOp(OpKernelConstruction* ctx) : OpKernel(ctx) {
    OP_REQUIRES_OK(ctx, ctx->GetAttr("N", &total_num_inputs_));
  }

  void Compute(OpKernelContext* ctx) override {
    OpInputList indices_t_all;
    OpInputList values_t_all;
    OpInputList dense_shape_t_all;
    OpInputList default_value_t_all;
    OP_REQUIRES_OK(ctx, ctx->input_list("indices", &indices_t_all));
    OP_REQUIRES_OK(ctx, ctx->input_list("values", &values_t_all));
    OP_REQUIRES_OK(ctx, ctx->input_list("dense_shape", &dense_shape_t_all));
    OP_REQUIRES_OK(ctx, ctx->input_list("default_value", &default_value_t_all));

    auto* range =
        ::hybridbackend::ProfilerRange::forLookup("SparseFillEmptyRowsN");

    for (size_t idx = 0; idx < total_num_inputs_; ++idx) {
      OP_REQUIRES(ctx,
                  TensorShapeUtils::IsVector(dense_shape_t_all[idx].shape()),
                  errors::InvalidArgument(
                      "dense_shape must be a vector, saw: ",
                      dense_shape_t_all[idx].shape().DebugString()));
      OP_REQUIRES(
          ctx, TensorShapeUtils::IsMatrix(indices_t_all[idx].shape()),
          errors::InvalidArgument("indices must be a matrix, saw: ",
                                  indices_t_all[idx].shape().DebugString()));
      OP_REQUIRES(
          ctx, TensorShapeUtils::IsVector(values_t_all[idx].shape()),
          errors::InvalidArgument("values must be a vector, saw: ",
                                  values_t_all[idx].shape().DebugString()));
      OP_REQUIRES(ctx,
                  TensorShapeUtils::IsScalar(default_value_t_all[idx].shape()),
                  errors::InvalidArgument(
                      "default_value must be a scalar, saw: ",
                      default_value_t_all[idx].shape().DebugString()));
    }

    std::vector<int64> dense_rows_all(total_num_inputs_);
    std::vector<int64> N_all(total_num_inputs_);
    std::vector<int> rank_all(total_num_inputs_);
    std::vector<Tensor*> empty_row_indicator_t_all(total_num_inputs_);
    std::vector<Tensor*> reverse_index_map_t_all(total_num_inputs_);
    std::vector<Tensor*> output_indices_t_all(total_num_inputs_);
    std::vector<Tensor*> output_values_t_all(total_num_inputs_);
    std::vector<size_t> idx_nonzero;

    for (size_t idx = 0; idx < total_num_inputs_; ++idx) {
      const int64 N = indices_t_all[idx].shape().dim_size(0);
      const int rank = indices_t_all[idx].shape().dim_size(1);
      const int64 dense_rows = dense_shape_t_all[idx].vec<int64>()(0);
      N_all[idx] = N;
      rank_all[idx] = rank;
      dense_rows_all[idx] = dense_rows;

      OP_REQUIRES_OK(
          ctx, ctx->allocate_output(2 * total_num_inputs_ + idx, {dense_rows},
                                    &empty_row_indicator_t_all[idx]));
      OP_REQUIRES_OK(ctx, ctx->allocate_output(3 * total_num_inputs_ + idx, {N},
                                               &reverse_index_map_t_all[idx]));
      if (TF_PREDICT_FALSE(dense_rows == 0)) {
        OP_REQUIRES(ctx, N == 0,
                    errors::InvalidArgument(
                        "Received SparseTensor with dense_shape[0] = "
                        "0 but indices.shape[0] = ",
                        N));
        OP_REQUIRES_OK(ctx, ctx->allocate_output(idx, {0, rank},
                                                 &output_indices_t_all[idx]));
        OP_REQUIRES_OK(ctx, ctx->allocate_output(total_num_inputs_ + idx, {0},
                                                 &output_values_t_all[idx]));

        continue;
      }
      idx_nonzero.push_back(idx);
    }

    int64 total_dense_rows = 0;
    for (size_t idx : idx_nonzero) {
      total_dense_rows += dense_rows_all[idx];
    }

    Tensor scratch_t;
    const int64 scratch_size = total_dense_rows + idx_nonzero.size();
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(
                            DT_INT64, TensorShape({scratch_size}), &scratch_t));
    int64* d_scratch = scratch_t.flat<int64>().data();
    int64* d_empty_row_indices_cursor = d_scratch;
    int64* d_num_empty_rows_cursor = d_scratch + total_dense_rows;

    std::vector<int64> dense_rows_nonzero(idx_nonzero.size());
    std::vector<int64> N_nonzero(idx_nonzero.size());
    std::vector<int> rank_nonzero(idx_nonzero.size());
    std::vector<T> default_value_nonzero(idx_nonzero.size());
    std::vector<const int64*> d_indices_nonzero(idx_nonzero.size());
    std::vector<const T*> d_values_nonzero(idx_nonzero.size());

    std::vector<Tensor*> empty_row_indicator_t_nonzero(idx_nonzero.size());
    std::vector<Tensor*> reverse_index_map_t_nonzero(idx_nonzero.size());
    std::vector<Tensor*> output_indices_t_nonzero(idx_nonzero.size());
    std::vector<Tensor*> output_values_t_nonzero(idx_nonzero.size());
    std::vector<bool*> d_empty_row_indicator_nonzero(idx_nonzero.size());
    std::vector<int64*> d_reverse_index_map_nonzero(idx_nonzero.size());
    std::vector<int64*> d_empty_row_indices_nonzero(idx_nonzero.size());
    std::vector<int64*> d_num_empty_rows_nonzero(idx_nonzero.size());
    for (size_t i = 0; i < idx_nonzero.size(); ++i) {
      const size_t idx = idx_nonzero[i];
      dense_rows_nonzero[i] = dense_rows_all[idx];
      N_nonzero[i] = N_all[idx];
      rank_nonzero[i] = rank_all[idx];
      default_value_nonzero[i] = default_value_t_all[idx].scalar<T>()();
      d_indices_nonzero[i] = indices_t_all[idx].flat<int64>().data();
      d_values_nonzero[i] = values_t_all[idx].flat<T>().data();
      d_empty_row_indicator_nonzero[i] =
          empty_row_indicator_t_all[idx]->flat<bool>().data();
      d_reverse_index_map_nonzero[i] =
          reverse_index_map_t_all[idx]->flat<int64>().data();
      d_empty_row_indices_nonzero[i] = d_empty_row_indices_cursor;
      d_empty_row_indices_cursor += dense_rows_all[idx];
      d_num_empty_rows_nonzero[i] = d_num_empty_rows_cursor;
      d_num_empty_rows_cursor++;
    }

    functor::SparseFillEmptyRowsNFunctors<T> functors;

    functors.build_n_empty_row_indices(
        idx_nonzero.size(), &N_nonzero[0], &rank_nonzero[0],
        &dense_rows_nonzero[0], &d_indices_nonzero[0], &d_values_nonzero[0],
        &d_empty_row_indicator_nonzero[0], &d_reverse_index_map_nonzero[0],
        &d_empty_row_indices_nonzero[0], &d_num_empty_rows_nonzero[0],
        ctx->eigen_device<GPUDevice>());

    std::vector<int64> num_empty_rows_nonzero(idx_nonzero.size());
    se::DeviceMemoryBase d_num_empty_rows_nonzero_ptr(
        d_scratch + total_dense_rows, idx_nonzero.size() * sizeof(int64));
    ctx->op_device_context()->stream()->ThenMemcpy(
        &num_empty_rows_nonzero[0], d_num_empty_rows_nonzero_ptr,
        idx_nonzero.size() * sizeof(int64));
    ctx->op_device_context()->stream()->BlockHostUntilDone();

    std::vector<size_t> idx_nonzero_actual;
    std::vector<int64> num_empty_rows_nonzero_actual;
    std::vector<int64*> d_empty_row_indices_nonzero_actual;
    for (size_t i = 0; i < idx_nonzero.size(); ++i) {
      const size_t idx = idx_nonzero[i];
      const int64 num_empty_rows = num_empty_rows_nonzero[i];
      num_empty_rows_nonzero_actual.push_back(num_empty_rows);
      d_empty_row_indices_nonzero_actual.push_back(
          d_empty_row_indices_nonzero[i]);
      if (num_empty_rows <= 0) {
        if (IsRefType(ctx->input_dtype(idx))) {
          ctx->forward_ref_input_to_ref_output(idx, idx);
        } else {
          ctx->set_output(idx, ctx->input(idx));
        }
        if (IsRefType(ctx->input_dtype(idx + total_num_inputs_))) {
          ctx->forward_ref_input_to_ref_output(idx + total_num_inputs_,
                                               idx + total_num_inputs_);
        } else {
          ctx->set_output(idx + total_num_inputs_,
                          ctx->input(idx + total_num_inputs_));
        }
        continue;
      }
      idx_nonzero_actual.push_back(idx);
    }

    std::vector<int64> N_nonzero_actual(idx_nonzero_actual.size());
    std::vector<int> rank_nonzero_actual(idx_nonzero_actual.size());
    std::vector<T> default_value_nonzero_actual(idx_nonzero_actual.size());
    std::vector<int64*> d_output_indices_nonzero_actual(
        idx_nonzero_actual.size());
    std::vector<T*> d_output_values_nonzero_actual(idx_nonzero_actual.size());
    for (size_t j = 0; j < idx_nonzero_actual.size(); ++j) {
      const size_t idx = idx_nonzero_actual[j];
      const int64 N = N_all[idx];
      const int rank = rank_all[idx];
      const int64 num_empty_rows = num_empty_rows_nonzero_actual[j];

      N_nonzero_actual[j] = N;
      rank_nonzero_actual[j] = rank;
      default_value_nonzero_actual[j] = default_value_t_all[idx].scalar<T>()();

      Tensor* output_indices_t;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(
                              idx, TensorShape({N + num_empty_rows, rank}),
                              &output_indices_t));
      int64* d_output_indices = output_indices_t->flat<int64>().data();
      d_output_indices_nonzero_actual[j] = d_output_indices;

      Tensor* output_values_t;
      OP_REQUIRES_OK(ctx,
                     ctx->allocate_output(total_num_inputs_ + idx,
                                          TensorShape({N + num_empty_rows}),
                                          &output_values_t));
      T* d_output_values = output_values_t->flat<T>().data();
      d_output_values_nonzero_actual[j] = d_output_values;

      se::DeviceMemoryBase output_indices_ptr(
          d_output_indices, (N + num_empty_rows) * rank * sizeof(int64));
      se::DeviceMemoryBase indices_ptr(
          const_cast<int64*>(indices_t_all[idx].flat<int64>().data()),
          N * rank * sizeof(int64));
      ctx->op_device_context()->stream()->ThenMemcpy(
          &output_indices_ptr, indices_ptr, N * rank * sizeof(int64));

      se::DeviceMemoryBase output_values_ptr(
          d_output_values, (N + num_empty_rows) * rank * sizeof(T));
      se::DeviceMemoryBase values_ptr(
          const_cast<T*>(values_t_all[idx].flat<T>().data()), N * sizeof(T));
      ctx->op_device_context()->stream()->ThenMemcpy(&output_values_ptr,
                                                     values_ptr, N * sizeof(T));

      se::DeviceMemoryBase empty_indices_ptr(
          d_output_indices + N * rank, num_empty_rows * rank * sizeof(int64));
      ctx->op_device_context()->stream()->ThenMemset32(
          &empty_indices_ptr, 0, num_empty_rows * rank * sizeof(int64));
    }

    functors.build_n_empty_rows(
        idx_nonzero_actual.size(), &N_nonzero_actual[0],
        &rank_nonzero_actual[0], &default_value_nonzero_actual[0],
        &num_empty_rows_nonzero_actual[0],
        &d_empty_row_indices_nonzero_actual[0],
        &d_output_indices_nonzero_actual[0], &d_output_values_nonzero_actual[0],
        ctx->eigen_device<GPUDevice>());

    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }

 private:
  int32 total_num_inputs_;
};

#define REGISTER_SPARSE_FILL_EMPTY_ROWS_N_KERNELS(TYPE)    \
  REGISTER_KERNEL_BUILDER(Name("HbSparseFillEmptyRowsN")   \
                              .Device(DEVICE_GPU)          \
                              .HostMemory("dense_shape")   \
                              .HostMemory("default_value") \
                              .TypeConstraint<TYPE>("T"),  \
                          SparseFillEmptyRowsNOp<TYPE>)

TF_CALL_SPARSE_FILL_EMPTY_ROWS_TYPES(REGISTER_SPARSE_FILL_EMPTY_ROWS_N_KERNELS);
#undef REGISTER_SPARSE_FILL_EMPTY_ROWS_N_KERNELS

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
