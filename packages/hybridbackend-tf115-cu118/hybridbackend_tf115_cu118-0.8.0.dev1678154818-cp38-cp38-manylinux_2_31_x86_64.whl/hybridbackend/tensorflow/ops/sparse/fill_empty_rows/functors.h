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
#ifndef HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_FILL_EMPTY_ROWS_FUNCTORS_H_
#define HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_FILL_EMPTY_ROWS_FUNCTORS_H_

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
#define TF_CALL_SPARSE_FILL_EMPTY_ROWS_TYPES(m)                         \
  TF_CALL_int64(m) TF_CALL_int32(m) TF_CALL_uint64(m) TF_CALL_uint32(m) \
      TF_CALL_float(m)

template <typename T>
struct SparseFillEmptyRowsFunctors {
 public:
  typedef T Type;

  SparseFillEmptyRowsFunctors(const int64 dense_rows, const int64 N,
                              const int rank, const T& default_value,
                              const int64* d_indices, const T* d_values,
                              bool* d_empty_row_indicator,
                              int64* d_reverse_index_map);

  void build_empty_row_indices(int64* d_empty_row_indices,
                               int64* d_num_empty_rows,
                               const Eigen::GpuDevice& d);
  void build_empty_rows(const int64 num_empty_rows, int64* d_empty_row_indices,
                        int64* d_output_indices, T* d_output_values,
                        const Eigen::GpuDevice& d);

 private:
  const int64 dense_rows_;
  const int64 N_;
  const int rank_;
  const T default_value_;
  const int64* d_indices_;
  const T* d_values_;
  bool* d_empty_row_indicator_;
  int64* d_reverse_index_map_;
};

template <typename T>
struct SparseFillEmptyRowsNFunctors {
 public:
  typedef T Type;

  void build_n_empty_row_indices(
      const size_t size, const int64* N_list, const int* rank_list,
      const int64* dense_rows_list, const int64** d_indices_list,
      const T** d_values_list, bool** d_empty_row_indicator_list,
      int64** d_reverse_index_map_list, int64** d_empty_row_indices_list,
      int64** d_num_empty_rows_list, const Eigen::GpuDevice& d);

  void build_n_empty_rows(const size_t actual_size, const int64* N_list,
                          const int* rank_list, const T* default_value_list,
                          const int64* num_empty_rows_list,
                          int64** d_empty_row_indices_list,
                          int64** d_output_indices_list,
                          T** d_output_values_list, const Eigen::GpuDevice& d);
};

#endif  // GOOGLE_CUDA

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
#endif  // HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_FILL_EMPTY_ROWS_FUNCTORS_H_
