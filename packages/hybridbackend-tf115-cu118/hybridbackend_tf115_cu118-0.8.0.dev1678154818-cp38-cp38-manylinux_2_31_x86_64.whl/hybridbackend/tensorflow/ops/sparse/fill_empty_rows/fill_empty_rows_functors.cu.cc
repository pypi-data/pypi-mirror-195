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
#include "hybridbackend/tensorflow/ops/sparse/fill_empty_rows/functors.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

namespace functor {

__global__ void SparseFillEmptyRowsInitializeIndicator(
    const int64 dense_rows, bool* d_empty_row_indicator,
    int64* d_num_empty_rows) {
  for (size_t idx : CudaGridRangeX(dense_rows)) {
    if (idx == 0) {
      *d_num_empty_rows = 0;
    }
    d_empty_row_indicator[idx] = true;
  }
}

__global__ void SparseFillEmptyRowsBuildIndicator(const int64 N, const int rank,
                                                  const int64* d_indices,
                                                  bool* d_empty_row_indicator,
                                                  int64* d_reverse_index_map) {
  for (size_t idx : CudaGridRangeX(N)) {
    d_empty_row_indicator[d_indices[idx * rank]] = false;
    d_reverse_index_map[idx] = idx;
  }
}

__global__ void SparseFillEmptyRowsBuildIndices(const int64 dense_rows,
                                                bool* d_empty_row_indicator,
                                                int64* d_empty_row_indices,
                                                int64* d_num_empty_rows) {
  for (size_t idx : CudaGridRangeX(dense_rows)) {
    if (d_empty_row_indicator[idx]) {
      d_empty_row_indices[atomicAdd(d_num_empty_rows, 1)] = idx;
    }
  }
}

template <typename T>
__global__ void SparseFillEmptyRowsDump(const int64 N, const int rank,
                                        const int64 num_empty_rows,
                                        const T default_value,
                                        int64* d_empty_row_indices,
                                        int64* d_output_indices,
                                        T* d_output_values) {
  for (size_t idx : CudaGridRangeX(num_empty_rows)) {
    d_output_values[N + idx] = default_value;
    d_output_indices[(N + idx) * rank] = d_empty_row_indices[idx];
  }
}

template <typename T>
SparseFillEmptyRowsFunctors<T>::SparseFillEmptyRowsFunctors(
    const int64 dense_rows, const int64 N, const int rank,
    const T& default_value, const int64* d_indices, const T* d_values,
    bool* d_empty_row_indicator, int64* d_reverse_index_map)
    : dense_rows_(dense_rows),
      N_(N),
      rank_(rank),
      default_value_(default_value),
      d_indices_(d_indices),
      d_values_(d_values),
      d_empty_row_indicator_(d_empty_row_indicator),
      d_reverse_index_map_(d_reverse_index_map) {}

template <typename T>
void SparseFillEmptyRowsFunctors<T>::build_empty_row_indices(
    int64* d_empty_row_indices, int64* d_num_empty_rows,
    const Eigen::GpuDevice& d) {
  if (TF_PREDICT_TRUE(dense_rows_ > 0)) {
    CudaLaunch(SparseFillEmptyRowsInitializeIndicator, dense_rows_, 0, d,
               nullptr, dense_rows_, d_empty_row_indicator_, d_num_empty_rows);
  }
  if (TF_PREDICT_TRUE(N_ > 0)) {
    CudaLaunch(SparseFillEmptyRowsBuildIndicator, N_, 0, d, nullptr, N_, rank_,
               d_indices_, d_empty_row_indicator_, d_reverse_index_map_);
  }
  if (TF_PREDICT_TRUE(dense_rows_ > 0)) {
    CudaLaunch(SparseFillEmptyRowsBuildIndices, dense_rows_, 0, d, nullptr,
               dense_rows_, d_empty_row_indicator_, d_empty_row_indices,
               d_num_empty_rows);
  }
}

template <typename T>
void SparseFillEmptyRowsFunctors<T>::build_empty_rows(
    const int64 num_empty_rows, int64* d_empty_row_indices,
    int64* d_output_indices, T* d_output_values, const Eigen::GpuDevice& d) {
  if (TF_PREDICT_TRUE(num_empty_rows > 0)) {
    CudaLaunch(SparseFillEmptyRowsDump<T>, num_empty_rows, 0, d, nullptr, N_,
               rank_, num_empty_rows, default_value_, d_empty_row_indices,
               d_output_indices, d_output_values);
  }
}

template struct SparseFillEmptyRowsFunctors<int32>;
template struct SparseFillEmptyRowsFunctors<int64>;
template struct SparseFillEmptyRowsFunctors<uint32>;
template struct SparseFillEmptyRowsFunctors<uint64>;
template struct SparseFillEmptyRowsFunctors<float>;

template <typename T>
void SparseFillEmptyRowsNFunctors<T>::build_n_empty_row_indices(
    const size_t size, const int64* N_list, const int* rank_list,
    const int64* dense_rows_list, const int64** d_indices_list,
    const T** d_values_list, bool** d_empty_row_indicator_list,
    int64** d_reverse_index_map_list, int64** d_empty_row_indices_list,
    int64** d_num_empty_rows_list, const Eigen::GpuDevice& d) {
  // TODO Implement fused CUDA kernel
  for (size_t idx = 0; idx < size; ++idx) {
    auto dense_rows = dense_rows_list[idx];
    if (TF_PREDICT_TRUE(dense_rows > 0)) {
      CudaLaunch(SparseFillEmptyRowsInitializeIndicator, dense_rows_list[idx],
                 0, d, nullptr, dense_rows_list[idx],
                 d_empty_row_indicator_list[idx], d_num_empty_rows_list[idx]);
    }
    auto N = N_list[idx];
    if (TF_PREDICT_TRUE(N > 0)) {
      CudaLaunch(SparseFillEmptyRowsBuildIndicator, N, 0, d, nullptr, N,
                 rank_list[idx], d_indices_list[idx],
                 d_empty_row_indicator_list[idx],
                 d_reverse_index_map_list[idx]);
    }
    if (TF_PREDICT_TRUE(dense_rows > 0)) {
      CudaLaunch(SparseFillEmptyRowsBuildIndices, dense_rows_list[idx], 0, d,
                 nullptr, dense_rows_list[idx], d_empty_row_indicator_list[idx],
                 d_empty_row_indices_list[idx], d_num_empty_rows_list[idx]);
    }
  }
}

template <typename T>
void SparseFillEmptyRowsNFunctors<T>::build_n_empty_rows(
    const size_t actual_size, const int64* N_list, const int* rank_list,
    const T* default_value_list, const int64* num_empty_rows_list,
    int64** d_empty_row_indices_list, int64** d_output_indices_list,
    T** d_output_values_list, const Eigen::GpuDevice& d) {
  // TODO Implement fused CUDA kernel
  for (size_t idx = 0; idx < actual_size; ++idx) {
    auto num_empty_rows = num_empty_rows_list[idx];
    if (TF_PREDICT_TRUE(num_empty_rows > 0)) {
      CudaLaunch(SparseFillEmptyRowsDump<T>, num_empty_rows, 0, d, nullptr,
                 N_list[idx], rank_list[idx], num_empty_rows,
                 default_value_list[idx], d_empty_row_indices_list[idx],
                 d_output_indices_list[idx], d_output_values_list[idx]);
    }
  }
}

template struct SparseFillEmptyRowsNFunctors<int32>;
template struct SparseFillEmptyRowsNFunctors<int64>;
template struct SparseFillEmptyRowsNFunctors<uint32>;
template struct SparseFillEmptyRowsNFunctors<uint64>;
template struct SparseFillEmptyRowsNFunctors<float>;

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
