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
#include "hybridbackend/tensorflow/ops/unique/hash_functors.h"

namespace tensorflow {
namespace hybridbackend {

REGISTER_OP("HbUniqueNByHash")
    .Input("x: N * T")
    .Output("y: N * T")
    .Output("idx: N * out_idx")
    .Attr("N: int >= 1")
    .Attr("T: {int32, int64, uint32, uint64}")
    .Attr("out_idx: {int32, int64} = DT_INT32")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      int32 num_columns;
      TF_RETURN_IF_ERROR(c->GetAttr("N", &num_columns));
      for (int i = 0; i < num_columns; ++i) {
        c->set_output(
            i, c->Vector(shape_inference::InferenceContext::kUnknownDim));
        c->set_output(i + num_columns, c->input(i));
        shape_inference::ShapeHandle dummy;
        TF_RETURN_IF_ERROR(c->WithRank(c->input(i), 1, &dummy));
      }
      return Status::OK();
    });

using GPUDevice = Eigen::GpuDevice;

template <typename T, typename TIndex>
class UniqueNByHashOp : public OpKernel {
 public:
  UniqueNByHashOp(OpKernelConstruction* ctx) : OpKernel(ctx) {
    OP_REQUIRES_OK(ctx, ctx->GetAttr("N", &total_num_inputs_));
  }

  void Compute(OpKernelContext* ctx) override {
    static double kLoadFactor =
        ::hybridbackend::EnvVarGetInt("HB_OP_UNIQUE_HASH_LFP", 50) / 100.0;

    auto* stream = ctx->op_device_context()->stream();

    OpInputList inputs;
    OP_REQUIRES_OK(ctx, ctx->input_list("x", &inputs));

    std::vector<TIndex> input_idx_vec;
    for (TIndex input_idx = 0; input_idx < total_num_inputs_; ++input_idx) {
      const Tensor& input = inputs[input_idx];
      OP_REQUIRES(ctx, input.NumElements() <= std::numeric_limits<int32>::max(),
                  errors::InvalidArgument(
                      "unique does not support input tensors larger than ",
                      std::numeric_limits<int32>::max(), " elements"));
      OP_REQUIRES(ctx, TensorShapeUtils::IsVector(input.shape()),
                  errors::InvalidArgument("unique expects a 1D vector."));

      if (TF_PREDICT_FALSE(input.NumElements() == 0)) {
        Tensor* output_ptr = nullptr;
        Tensor* output_idx_ptr = nullptr;
        OP_REQUIRES_OK(ctx, ctx->allocate_output(input_idx, {0}, &output_ptr));
        OP_REQUIRES_OK(ctx, ctx->allocate_output(total_num_inputs_ + input_idx,
                                                 {0}, &output_idx_ptr));
        continue;
      }

      input_idx_vec.push_back(input_idx);
    }

    const int64 num_inputs = static_cast<int64>(input_idx_vec.size());
    if (TF_PREDICT_FALSE(num_inputs == 0)) {
      return;
    }

    AllocatorAttributes host_alloc_attrs;
    host_alloc_attrs.set_on_host(true);
    host_alloc_attrs.set_gpu_compatible(true);

    auto* range = ::hybridbackend::ProfilerRange::forLookup("UniqueN");

    // Populate sizes
    const int64 n_buffer_sizes = num_inputs;
    const int64 n_input_sizes = num_inputs;
    const int64 n_output_sizes = num_inputs;
    const int64 n_sizes = n_buffer_sizes + n_input_sizes + n_output_sizes;

    Tensor h_sizes_tensor;
    OP_REQUIRES_OK(ctx,
                   ctx->allocate_temp(DataTypeToEnum<TIndex>::value, {n_sizes},
                                      &h_sizes_tensor, host_alloc_attrs));
    TIndex* h_sizes = h_sizes_tensor.flat<TIndex>().data();
    TIndex* h_buffer_sizes = h_sizes;
    TIndex* h_input_sizes = h_buffer_sizes + n_buffer_sizes;
    TIndex* h_output_sizes = h_input_sizes + n_input_sizes;

    TIndex total_buffer_size = 0;
    for (TIndex i = 0; i < num_inputs; ++i) {
      const TIndex input_idx = input_idx_vec[i];
      const TIndex input_size = inputs[input_idx].NumElements();
      const TIndex buffer_size = static_cast<TIndex>(input_size / kLoadFactor);
      total_buffer_size += buffer_size;
      h_buffer_sizes[i] = buffer_size;
      h_input_sizes[i] = input_size;
      h_output_sizes[i] = -1;
    }

    Tensor d_output_sizes_tensor;
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DataTypeToEnum<TIndex>::value, {n_output_sizes},
                                &d_output_sizes_tensor));
    TIndex* d_output_sizes = d_output_sizes_tensor.flat<TIndex>().data();

    // Allocate buffers
    Tensor d_input_buffer_tensor;
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DataTypeToEnum<T>::value, {total_buffer_size},
                                &d_input_buffer_tensor));
    T* d_input_buffer = d_input_buffer_tensor.flat<T>().data();

    Tensor d_index_buffer_tensor;
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DataTypeToEnum<TIndex>::value,
                                {total_buffer_size}, &d_index_buffer_tensor));
    TIndex* d_index_buffer = d_index_buffer_tensor.flat<TIndex>().data();

    // Allocate buffer pointers
    const int64 n_input_buffers = sizeof(T*) * num_inputs;
    const int64 n_index_buffers = sizeof(TIndex*) * num_inputs;
    const int64 n_buffers = n_input_buffers + n_index_buffers;

    Tensor hd_buffers_tensor;
    OP_REQUIRES_OK(ctx,
                   ctx->allocate_temp(DT_INT8, {n_buffers}, &hd_buffers_tensor,
                                      host_alloc_attrs));
    int8* h_buffers = hd_buffers_tensor.flat<int8>().data();
    T** hd_input_buffers = reinterpret_cast<T**>(h_buffers);
    TIndex** hd_index_buffers =
        reinterpret_cast<TIndex**>(h_buffers + n_input_buffers);

    for (TIndex i = 0; i < num_inputs; ++i) {
      if (i == 0) {
        hd_input_buffers[i] = d_input_buffer;
        hd_index_buffers[i] = d_index_buffer;
      } else {
        const TIndex buffer_size = h_buffer_sizes[i - 1];
        hd_input_buffers[i] = hd_input_buffers[i - 1] + buffer_size;
        hd_index_buffers[i] = hd_index_buffers[i - 1] + buffer_size;
      }
    }

    // Allocate inputs and outputs pointers
    const int64 input_ptrs_size = sizeof(T*) * num_inputs;
    Tensor hd_inputs_tensor;
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DT_INT8, {input_ptrs_size}, &hd_inputs_tensor,
                                host_alloc_attrs));
    const T** hd_inputs =
        reinterpret_cast<const T**>(hd_inputs_tensor.flat<int8>().data());

    const int64 index_ptrs_size = sizeof(TIndex*) * num_inputs;
    Tensor hd_output_indices_tensor;
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DT_INT8, {index_ptrs_size},
                                &hd_output_indices_tensor, host_alloc_attrs));
    TIndex** hd_output_indices = reinterpret_cast<TIndex**>(
        hd_output_indices_tensor.flat<int8>().data());

    for (TIndex i = 0; i < num_inputs; ++i) {
      const TIndex input_idx = input_idx_vec[i];
      const Tensor& input = inputs[input_idx];
      const TIndex input_size = input.NumElements();
      hd_inputs[i] = input.flat<T>().data();
      Tensor* output_indices = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(total_num_inputs_ + input_idx,
                                               {input_size}, &output_indices));
      hd_output_indices[i] = output_indices->flat<TIndex>().data();
    }

    // Phase 1: Initialize and insert keys
    functor::UniqueNByHash<T, TIndex> unique_n_by_hash(
        hd_input_buffers, hd_index_buffers, h_buffer_sizes, hd_inputs,
        h_input_sizes, num_inputs);
    unique_n_by_hash(d_output_sizes, hd_output_indices, nullptr,
                     ctx->eigen_device<GPUDevice>());

    // Allocate outputs
    se::DeviceMemoryBase d_output_sizes_mem(d_output_sizes,
                                            d_output_sizes_tensor.TotalBytes());
    stream->ThenMemcpy(h_output_sizes, d_output_sizes_mem,
                       d_output_sizes_tensor.TotalBytes());

    Tensor hd_outputs_tensor;
    OP_REQUIRES_OK(
        ctx, ctx->allocate_temp(DT_INT8, {input_ptrs_size}, &hd_outputs_tensor,
                                host_alloc_attrs));
    T** hd_outputs =
        reinterpret_cast<T**>(hd_outputs_tensor.flat<int8>().data());

    stream->BlockHostUntilDone();
    for (TIndex i = 0; i < num_inputs; ++i) {
      const TIndex input_idx = input_idx_vec[i];
      Tensor* output_tensor = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(input_idx, {h_output_sizes[i]},
                                               &output_tensor));
      hd_outputs[i] = output_tensor->flat<T>().data();
    }

    // Phase 2: Dump keys to outputs
    unique_n_by_hash(nullptr, nullptr, hd_outputs,
                     ctx->eigen_device<GPUDevice>());

    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }

 private:
  int32 total_num_inputs_;
};

#define REGISTER_HASH_UNIQUE_N_KERNEL_INT32(T)                   \
  REGISTER_KERNEL_BUILDER(Name("HbUniqueNByHash")                \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<T>("T")            \
                              .TypeConstraint<int32>("out_idx"), \
                          UniqueNByHashOp<T, int32>)

TF_CALL_int32(REGISTER_HASH_UNIQUE_N_KERNEL_INT32);
TF_CALL_int64(REGISTER_HASH_UNIQUE_N_KERNEL_INT32);
TF_CALL_uint32(REGISTER_HASH_UNIQUE_N_KERNEL_INT32);
TF_CALL_uint64(REGISTER_HASH_UNIQUE_N_KERNEL_INT32);
#undef REGISTER_HASH_UNIQUE_N_KERNEL_INT32

#define REGISTER_HASH_UNIQUE_N_KERNEL_INT64(T)                   \
  REGISTER_KERNEL_BUILDER(Name("HbUniqueNByHash")                \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<T>("T")            \
                              .TypeConstraint<int64>("out_idx"), \
                          UniqueNByHashOp<T, int64>)

TF_CALL_int32(REGISTER_HASH_UNIQUE_N_KERNEL_INT64);
TF_CALL_int64(REGISTER_HASH_UNIQUE_N_KERNEL_INT64);
TF_CALL_uint32(REGISTER_HASH_UNIQUE_N_KERNEL_INT64);
TF_CALL_uint64(REGISTER_HASH_UNIQUE_N_KERNEL_INT64);
#undef REGISTER_HASH_UNIQUE_N_KERNEL_INT64

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
