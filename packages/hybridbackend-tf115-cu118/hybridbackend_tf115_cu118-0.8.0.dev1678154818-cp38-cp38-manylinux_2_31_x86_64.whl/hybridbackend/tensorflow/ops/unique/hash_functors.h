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
#ifndef HYBRIDBACKEND_TENSORFLOW_OPS_UNIQUE_HASH_FUNCTORS_H_
#define HYBRIDBACKEND_TENSORFLOW_OPS_UNIQUE_HASH_FUNCTORS_H_

#if HYBRIDBACKEND_TENSORFLOW

#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/framework/tensor_reference.h>
#include <tensorflow/core/public/version.h>

#if GOOGLE_CUDA
#include <cuda.h>
#include <cuda_runtime.h>
#endif

namespace tensorflow {

class OpKernelContext;

namespace hybridbackend {
namespace functor {

#if GOOGLE_CUDA
template <typename T, typename TIndex>
struct UniqueByHash {
 public:
  typedef T Type;
  typedef typename std::make_unsigned<T>::type UnsignedType;
  typedef TIndex IndexType;

  UniqueByHash(T* d_input_buffer, TIndex* d_index_buffer,
               const TIndex buffer_size, const T* d_input,
               const TIndex input_size);
  void operator()(TIndex* d_output_size, TIndex* d_output_idx, T* d_output,
                  const Eigen::GpuDevice& d);

 private:
  T* d_input_buffer_;
  TIndex* d_index_buffer_;
  const TIndex buffer_size_;
  const T* d_input_;
  const TIndex input_size_;
};

template <typename T, typename TIndex>
struct UniqueNByHash {
 public:
  typedef T Type;
  typedef typename std::make_unsigned<T>::type UnsignedType;
  typedef TIndex IndexType;

  UniqueNByHash(T** hd_input_buffers, TIndex** hd_index_buffers,
                const TIndex* h_buffer_sizes, const T** hd_inputs,
                const TIndex* h_input_sizes, const TIndex num_inputs);
  void operator()(TIndex* d_output_size, TIndex** hd_output_indices,
                  T** hd_outputs, const Eigen::GpuDevice& d);

 private:
  T** hd_input_buffers_;
  TIndex** hd_index_buffers_;
  const TIndex* h_buffer_sizes_;
  const T** hd_inputs_;
  const TIndex* h_input_sizes_;
  const TIndex num_inputs_;
  TIndex max_buffer_size_;
  TIndex total_max_buffer_size_;
};

#endif  // GOOGLE_CUDA

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
#endif  // HYBRIDBACKEND_TENSORFLOW_OPS_UNIQUE_HASH_FUNCTORS_H_
