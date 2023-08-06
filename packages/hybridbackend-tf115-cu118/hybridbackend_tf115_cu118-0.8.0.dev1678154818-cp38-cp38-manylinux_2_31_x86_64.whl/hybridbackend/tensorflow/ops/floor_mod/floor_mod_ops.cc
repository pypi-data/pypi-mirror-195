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
#include "hybridbackend/tensorflow/ops/floor_mod/functors.h"

namespace tensorflow {
namespace hybridbackend {

REGISTER_OP("HbFloorMod")
    .Input("x: T")
    .Input("y: T")
    .Output("z: T")
    .Attr("T: {int32, int64}")
    .SetShapeFn(shape_inference::BroadcastBinaryOpShapeFn);

using GPUDevice = Eigen::GpuDevice;

template <typename T>
class FloorModOp : public OpKernel {
 public:
  FloorModOp(OpKernelConstruction* ctx) : OpKernel(ctx) {}

  void Compute(OpKernelContext* ctx) override {
    const Tensor* x_tensor;
    OP_REQUIRES_OK(ctx, ctx->input("x", &x_tensor));
    const T* d_x = x_tensor->flat<T>().data();
    const int64 x_size = x_tensor->NumElements();
    const Tensor* y_tensor;
    OP_REQUIRES_OK(ctx, ctx->input("y", &y_tensor));
    const T* d_y = y_tensor->flat<T>().data();
    const int64 y_size = y_tensor->NumElements();

    if (TF_PREDICT_FALSE(x_size == 0)) {
      Tensor* z_tensor = nullptr;
      OP_REQUIRES_OK(ctx,
                     ctx->allocate_output(0, x_tensor->shape(), &z_tensor));
      return;
    }

    OP_REQUIRES(
        ctx, y_size == x_size || y_size == 1,
        errors::InvalidArgument("FloorMod requires broadcasting shape."));

    functor::FloorModFunctors<T> functors(x_size);
    auto* range = ::hybridbackend::ProfilerRange::forLookup("FloorMod");
    Tensor* z_tensor = nullptr;
    OP_REQUIRES_OK(ctx, ctx->allocate_output(0, x_tensor->shape(), &z_tensor));
    T* d_z = z_tensor->flat<T>().data();

    if (y_size == x_size) {
      functors.floor_mod_all(d_x, d_y, d_z, ctx->eigen_device<GPUDevice>());
    } else {
      functors.floor_mod_one(d_x, d_y, d_z, ctx->eigen_device<GPUDevice>());
    }

    ctx->device()->tensorflow_gpu_device_info()->event_mgr->ThenExecute(
        ctx->op_device_context()->stream(), [range]() { delete range; });
  }
};

#define REGISTER_FLOOR_MOD_KERNEL(T)                                \
  REGISTER_KERNEL_BUILDER(                                          \
      Name("HbFloorMod").Device(DEVICE_GPU).TypeConstraint<T>("T"), \
      FloorModOp<T>)
TF_CALL_int32(REGISTER_FLOOR_MOD_KERNEL);
TF_CALL_int64(REGISTER_FLOOR_MOD_KERNEL);
#undef REGISTER_FLOOR_MOD_KERNEL

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
