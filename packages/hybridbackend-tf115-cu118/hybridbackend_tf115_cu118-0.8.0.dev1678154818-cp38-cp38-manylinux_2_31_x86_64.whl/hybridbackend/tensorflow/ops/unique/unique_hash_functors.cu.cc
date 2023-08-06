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
#include "hybridbackend/tensorflow/ops/unique/hash_functors.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

namespace functor {
template <typename T, typename TIndex>
__global__ void UniqueByHashInitialize(TIndex* d_output_size, T* d_input_buffer,
                                       TIndex* d_index_buffer,
                                       const TIndex buffer_size) {
  const TIndex idx = blockIdx.x * blockDim.x + threadIdx.x;

  if (0 == idx) {
    *d_output_size = 0;
  }
  if (idx < buffer_size) {
    static __constant__ T kInputNil = std::numeric_limits<T>::max();
    static __constant__ TIndex kIndexNil = std::numeric_limits<TIndex>::min();

    d_input_buffer[idx] = kInputNil;
    d_index_buffer[idx] = kIndexNil;
  }
}

template <typename T, typename TIndex>
__global__ void UniqueByHashInsert(TIndex* d_output_size, TIndex* d_output_idx,
                                   T* d_input_buffer, TIndex* d_index_buffer,
                                   const TIndex buffer_size, const T* d_input,
                                   const TIndex input_size) {
  const TIndex idx = blockIdx.x * blockDim.x + threadIdx.x;

  if (idx < input_size) {
    static __constant__ T kInputNil = std::numeric_limits<T>::max();
    static __constant__ TIndex kIndexNil = std::numeric_limits<TIndex>::min();

    const T input = d_input[idx] % kInputNil;
    size_t slot = murmur3_hash32(input) % buffer_size;
    while (true) {  // linear probe
      const T probe_input = atomicCAS(d_input_buffer + slot, kInputNil, input);
      volatile TIndex& probe_index = d_index_buffer[slot];
      if (kInputNil == probe_input) {
        TIndex new_index = atomicAdd(d_output_size, 1);
        d_output_idx[idx] = new_index;
        probe_index = new_index;
        break;
      } else if (input == probe_input) {
        while (kIndexNil == probe_index)
          ;
        d_output_idx[idx] = probe_index;
        break;
      }
      slot = (slot + 1) % buffer_size;
    }
  }
}

template <typename T, typename TIndex>
__global__ void UniqueByHashDump(T* d_output, T* d_input_buffer,
                                 TIndex* d_index_buffer,
                                 const TIndex buffer_size) {
  const TIndex idx = blockIdx.x * blockDim.x + threadIdx.x;

  if (idx < buffer_size) {
    static __constant__ T kInputNil = std::numeric_limits<T>::max();

    const T read_input = d_input_buffer[idx];
    if (kInputNil != read_input) {
      d_output[d_index_buffer[idx]] = read_input;
    }
  }
}

template <typename T, typename TIndex>
UniqueByHash<T, TIndex>::UniqueByHash(T* d_input_buffer, TIndex* d_index_buffer,
                                      const TIndex buffer_size,
                                      const T* d_input, const TIndex input_size)
    : d_input_buffer_(d_input_buffer),
      d_index_buffer_(d_index_buffer),
      buffer_size_(buffer_size),
      d_input_(d_input),
      input_size_(input_size) {}

template <typename T, typename TIndex>
void UniqueByHash<T, TIndex>::operator()(TIndex* d_output_size,
                                         TIndex* d_output_idx, T* d_output,
                                         const Eigen::GpuDevice& d) {
  if (nullptr == d_output) {
    CudaLaunchSafe(UniqueByHashInitialize<T, TIndex>, buffer_size_, 0, d,
                   nullptr, d_output_size, d_input_buffer_, d_index_buffer_,
                   buffer_size_);
    CudaLaunchSafe(UniqueByHashInsert<T, TIndex>, input_size_, 0, d, nullptr,
                   d_output_size, d_output_idx, d_input_buffer_,
                   d_index_buffer_, buffer_size_, d_input_, input_size_);
  } else {
    CudaLaunchSafe(UniqueByHashDump<T, TIndex>, buffer_size_, 0, d, nullptr,
                   d_output, d_input_buffer_, d_index_buffer_, buffer_size_);
  }
}

template struct UniqueByHash<int32, int32>;
template struct UniqueByHash<int64, int32>;
template struct UniqueByHash<uint32, int32>;
template struct UniqueByHash<uint64, int32>;
template struct UniqueByHash<int32, int64>;
template struct UniqueByHash<int64, int64>;
template struct UniqueByHash<uint32, int64>;
template struct UniqueByHash<uint64, int64>;

template <typename T, typename TIndex>
UniqueNByHash<T, TIndex>::UniqueNByHash(T** hd_input_buffers,
                                        TIndex** hd_index_buffers,
                                        const TIndex* h_buffer_sizes,
                                        const T** hd_inputs,
                                        const TIndex* h_input_sizes,
                                        const TIndex num_inputs)
    : hd_input_buffers_(hd_input_buffers),
      hd_index_buffers_(hd_index_buffers),
      h_buffer_sizes_(h_buffer_sizes),
      hd_inputs_(hd_inputs),
      h_input_sizes_(h_input_sizes),
      num_inputs_(num_inputs),
      max_buffer_size_(0),
      total_max_buffer_size_(0) {
  for (size_t i = 0; i < num_inputs_; ++i) {
    const auto& buffer_size = h_buffer_sizes_[i];
    if (buffer_size > max_buffer_size_) {
      max_buffer_size_ = buffer_size;
    }
  }
  total_max_buffer_size_ = num_inputs_ * max_buffer_size_;
}

template <typename T, typename TIndex>
void UniqueNByHash<T, TIndex>::operator()(TIndex* d_output_sizes,
                                          TIndex** hd_output_indices,
                                          T** hd_outputs,
                                          const Eigen::GpuDevice& d) {
  if (nullptr == hd_outputs) {
    for (size_t i = 0; i < num_inputs_; ++i) {
      const TIndex buffer_size = h_buffer_sizes_[i];
      const TIndex input_size = h_input_sizes_[i];
      TIndex* d_output_size = d_output_sizes + i;
      T* hd_input_buffer = hd_input_buffers_[i];
      TIndex* hd_index_buffer = hd_index_buffers_[i];
      CudaLaunchSafe(UniqueByHashInitialize<T, TIndex>, buffer_size, 0, d,
                     nullptr, d_output_size, hd_input_buffer, hd_index_buffer,
                     buffer_size);
      CudaLaunchSafe(UniqueByHashInsert<T, TIndex>, input_size, 0, d, nullptr,
                     d_output_size, hd_output_indices[i], hd_input_buffer,
                     hd_index_buffer, buffer_size, hd_inputs_[i], input_size);
    }
  } else {
    for (size_t i = 0; i < num_inputs_; ++i) {
      const TIndex buffer_size = h_buffer_sizes_[i];
      CudaLaunchSafe(UniqueByHashDump<T, TIndex>, buffer_size, 0, d, nullptr,
                     hd_outputs[i], hd_input_buffers_[i], hd_index_buffers_[i],
                     buffer_size);
    }
  }
}

template struct UniqueNByHash<int32, int32>;
template struct UniqueNByHash<int64, int32>;
template struct UniqueNByHash<uint32, int32>;
template struct UniqueNByHash<uint64, int32>;
template struct UniqueNByHash<int32, int64>;
template struct UniqueNByHash<int64, int64>;
template struct UniqueNByHash<uint32, int64>;
template struct UniqueNByHash<uint64, int64>;

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
