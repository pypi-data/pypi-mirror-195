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

REGISTER_OP("HbUniqueByHash")
    .Input("x: T")
    .Output("y: T")
    .Output("idx: out_idx")
    .Attr("T: {int32, int64, uint32, uint64}")
    .Attr("out_idx: {int32, int64} = DT_INT32")
    .SetShapeFn([](shape_inference::InferenceContext* c) {
      c->set_output(0,
                    c->Vector(shape_inference::InferenceContext::kUnknownDim));
      c->set_output(1, c->input(0));
      // Assert that the input rank is 1.
      shape_inference::ShapeHandle dummy;
      return c->WithRank(c->input(0), 1, &dummy);
    });

using GPUDevice = Eigen::GpuDevice;

template <typename T, typename TIndex>
class UniqueByHashOp : public OpKernel {
 public:
  UniqueByHashOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    static double kLoadFactor =
        ::hybridbackend::EnvVarGetInt("HB_OP_UNIQUE_HASH_LFP", 50) / 100.0;

    auto* stream = ctx->op_device_context()->stream();

    const Tensor& input = ctx->input(0);
    const T* d_input = input.flat<T>().data();

    OP_REQUIRES(ctx, input.NumElements() <= std::numeric_limits<int32>::max(),
                errors::InvalidArgument(
                    "unique does not support input tensors larger than ",
                    std::numeric_limits<int32>::max(), " elements"));
    OP_REQUIRES(ctx, TensorShapeUtils::IsVector(input.shape()),
                errors::InvalidArgument("unique expects a 1D vector."));

    TIndex input_size = input.NumElements();
    if (TF_PREDICT_FALSE(input_size == 0)) {
      Tensor* output_ptr = nullptr;
      Tensor* output_idx_ptr = nullptr;
      OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {0}, &output_ptr));
      OP_REQUIRES_OK(ctx, ctx->allocate_output(1, {0}, &output_idx_ptr));
      return;
    }

    auto* range = ::hybridbackend::ProfilerRange::forLookup("Unique");
    TIndex buffer_size = static_cast<TIndex>(input_size / kLoadFactor);

    Tensor input_buffer;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DataTypeToEnum<T>::value,
                                           {buffer_size}, &input_buffer));
    T* d_input_buffer = input_buffer.flat<T>().data();

    Tensor index_buffer;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DataTypeToEnum<TIndex>::value,
                                           {buffer_size}, &index_buffer));
    TIndex* d_index_buffer = index_buffer.flat<TIndex>().data();

    Tensor output_size;
    OP_REQUIRES_OK(ctx, ctx->allocate_temp(DataTypeToEnum<TIndex>::value,
                                           TensorShape({}), &output_size));
    TIndex* d_output_size = output_size.flat<TIndex>().data();

    functor::UniqueByHash<T, TIndex> unique_by_hash(
        d_input_buffer, d_index_buffer, buffer_size, d_input, input_size);

    Tensor* output_idx_ptr = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(1, {input_size}, &output_idx_ptr));
    TIndex* d_output_idx = output_idx_ptr->flat<TIndex>().data();

    unique_by_hash(d_output_size, d_output_idx, nullptr,
                   ctx->eigen_device<GPUDevice>());
    se::DeviceMemoryBase output_size_ptr(d_output_size, sizeof(TIndex));
    TIndex h_output_size;
    stream->ThenMemcpy(&h_output_size, output_size_ptr, sizeof(TIndex));
    stream->BlockHostUntilDone();
    Tensor* output_ptr = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, {h_output_size}, &output_ptr));
    T* d_output = output_ptr->flat<T>().data();
    unique_by_hash(nullptr, nullptr, d_output, ctx->eigen_device<GPUDevice>());
    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }
};

#define REGISTER_HASH_UNIQUE_KERNEL_INT32(T)                     \
  REGISTER_KERNEL_BUILDER(Name("HbUniqueByHash")                 \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<T>("T")            \
                              .TypeConstraint<int32>("out_idx"), \
                          UniqueByHashOp<T, int32>)

TF_CALL_int32(REGISTER_HASH_UNIQUE_KERNEL_INT32);
TF_CALL_int64(REGISTER_HASH_UNIQUE_KERNEL_INT32);
TF_CALL_uint32(REGISTER_HASH_UNIQUE_KERNEL_INT32);
TF_CALL_uint64(REGISTER_HASH_UNIQUE_KERNEL_INT32);
#undef REGISTER_HASH_UNIQUE_KERNEL_INT32

#define REGISTER_HASH_UNIQUE_KERNEL_INT64(T)                     \
  REGISTER_KERNEL_BUILDER(Name("HbUniqueByHash")                 \
                              .Device(DEVICE_GPU)                \
                              .TypeConstraint<T>("T")            \
                              .TypeConstraint<int64>("out_idx"), \
                          UniqueByHashOp<T, int64>)

TF_CALL_int32(REGISTER_HASH_UNIQUE_KERNEL_INT64);
TF_CALL_int64(REGISTER_HASH_UNIQUE_KERNEL_INT64);
TF_CALL_uint32(REGISTER_HASH_UNIQUE_KERNEL_INT64);
TF_CALL_uint64(REGISTER_HASH_UNIQUE_KERNEL_INT64);
#undef REGISTER_HASH_UNIQUE_KERNEL_INT64

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
