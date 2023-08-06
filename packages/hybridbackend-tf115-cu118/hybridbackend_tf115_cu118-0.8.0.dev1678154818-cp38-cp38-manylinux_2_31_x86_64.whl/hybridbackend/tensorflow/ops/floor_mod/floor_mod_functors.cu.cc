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

#include <limits>

#include <tensorflow/core/framework/register_types.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/public/version.h>

#include "hybridbackend/common/atomic.cu.h"
#include "hybridbackend/common/murmur3.cu.h"

#include "hybridbackend/tensorflow/common/device_functions.h"
#include "hybridbackend/tensorflow/ops/floor_mod/functors.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

namespace functor {
template <typename T>
__global__ void FloorModAllKernel(const int64 N, const T* d_x, const T* d_y,
                                  T* d_z) {
  for (size_t idx : CudaGridRangeX(N)) {
    const T y = d_y[idx];
    d_z[idx] = (d_x[idx] % y + y) % y;
  }
}

template <typename T>
__global__ void FloorModOneKernel(const int64 N, const T* d_x, const T* d_y,
                                  T* d_z) {
  for (size_t idx : CudaGridRangeX(N)) {
    const T y = *d_y;
    d_z[idx] = (d_x[idx] % y + y) % y;
  }
}

template <typename T>
FloorModFunctors<T>::FloorModFunctors(const int64 size) : size_(size) {}

template <typename T>
void FloorModFunctors<T>::floor_mod_all(const T* d_x, const T* d_y, T* d_z,
                                        const Eigen::GpuDevice& d) {
  CudaLaunch(FloorModAllKernel<T>, size_, 0, d, nullptr, size_, d_x, d_y, d_z);
}

template <typename T>
void FloorModFunctors<T>::floor_mod_one(const T* d_x, const T* d_y, T* d_z,
                                        const Eigen::GpuDevice& d) {
  CudaLaunch(FloorModOneKernel<T>, size_, 0, d, nullptr, size_, d_x, d_y, d_z);
}

template struct FloorModFunctors<int32>;
template struct FloorModFunctors<int64>;

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
