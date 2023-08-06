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

#include <thrust/device_ptr.h>
#include <thrust/device_vector.h>

#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/register_types.h>
#include <tensorflow/core/framework/shape_inference.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/public/version.h>

#include "hybridbackend/common/atomic.cu.h"
#include "hybridbackend/tensorflow/common/device_functions.h"
#include "hybridbackend/tensorflow/common/fusion_helper.cu.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/common.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

namespace functor {

template <typename Index>
void FindMaxSegId<Index>::operator()(OpKernelContext* ctx,
                                     const Tensor* seg_ids, Index& max_id) {
  AllocatorAttributes attr;
  attr.set_on_host(true);
  attr.set_gpu_compatible(true);
  Tensor seg_ids_cpu;
  ctx->allocate_temp(seg_ids->dtype(), TensorShape{seg_ids->NumElements()},
                     &seg_ids_cpu, attr);
  if (!ctx->status().ok()) {
    return;
  }
  auto dst_vec = seg_ids_cpu.flat<Index>();
  auto src_vec = seg_ids->flat<Index>();

  // copy data
  auto* stream = ctx->op_device_context()->stream();
  ctx->op_device_context()->stream()->ThenMemcpy(
      const_cast<char*>(seg_ids_cpu.tensor_data().data()),
      se::DeviceMemoryBase(const_cast<char*>(seg_ids->tensor_data().data()),
                           seg_ids->TotalBytes()),
      seg_ids->TotalBytes());
  stream->BlockHostUntilDone();
  // find the max
  max_id = *std::max_element(dst_vec.data(),
                             dst_vec.data() + seg_ids->NumElements());
}

#define DEFINE_FIND_MAX_SEGMENT_ID(Index) template struct FindMaxSegId<Index>;

TF_CALL_SEGMENT_REDUCTION_INDEX_TYPES(DEFINE_FIND_MAX_SEGMENT_ID);

template <typename T, typename Index>
__global__ void SparseSegmentSumNKernel(const Cuda2DLaunchConfig config,
                                        int64* data_sparse_size,
                                        int64* output_total_size,
                                        int64* data_inner_dim, T** data,
                                        Index** indices, int32** seg_ids,
                                        T** output) {
  CUDA_AXIS_KERNEL_LOOP(g_idx, config.virtual_thread_count.y, Y) {
    CUDA_AXIS_KERNEL_LOOP(g_offset, config.virtual_thread_count.x, X) {
      if (g_offset < data_sparse_size[g_idx]) {
        const int64 data_inner_dim_thd = data_inner_dim[g_idx];
        const int64 sparse_row = g_offset / data_inner_dim_thd;
        const int64 sparse_offset = g_offset % data_inner_dim_thd;
        const Index data_row = indices[g_idx][sparse_row];
        const int64 data_idx = data_row * data_inner_dim_thd + sparse_offset;
        const int32 output_row = seg_ids[g_idx][sparse_row];
        const int64 output_idx =
            output_row * data_inner_dim_thd + sparse_offset;
        if (output_idx < 0 || output_idx >= output_total_size[g_idx]) {
          continue;
        }
        CudaAtomicAdd(output[g_idx] + output_idx, ldg(data[g_idx] + data_idx));
      }
    }
  }
}

template <typename T, typename Index>
__global__ void SparseSegmentNLenSumKernel(const Cuda2DLaunchConfig config,
                                           int64* num_ids,
                                           int64* output_row_size,
                                           Index** seg_ids, Index** seg_lens) {
  CUDA_AXIS_KERNEL_LOOP(g_idx, config.virtual_thread_count.y, Y) {
    CUDA_AXIS_KERNEL_LOOP(g_offset, config.virtual_thread_count.x, X) {
      if (g_offset < num_ids[g_idx]) {
        const Index output_idx = seg_ids[g_idx][g_offset];
        if (output_idx < 0 || output_idx >= output_row_size[g_idx]) {
          continue;
        }
        CudaAtomicAdd(seg_lens[g_idx] + output_idx, Index(1));
      }
    }
  }
}

template <typename T, typename Index>
void SparseSegmentReductionNFunctors<T, Index>::sum(
    int64 max_output_total_size, int32 valid_num_columns,
    int64* output_total_sizes_dev, int8* outputs_ptr_heads_dev,
    int64 max_data_sparse_size, int64* data_sparse_sizes_dev,
    int64* data_inner_dims_dev, int8* data_ptr_heads_dev,
    int8* indices_ptr_heads_dev, int8* segids_ptr_heads_dev,
    const Eigen::GpuDevice& d) {
  Cuda2DLaunchConfig conf2d =
      GetCuda2DLaunchConfig(max_output_total_size, valid_num_columns, d);
  SetToNValue<T, int64>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, output_total_sizes_dev,
          reinterpret_cast<T**>(outputs_ptr_heads_dev), T(0.0));
  conf2d = GetCuda2DLaunchConfig(max_data_sparse_size, valid_num_columns, d);
  SparseSegmentSumNKernel<T, Index>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, data_sparse_sizes_dev, output_total_sizes_dev,
          data_inner_dims_dev, reinterpret_cast<T**>(data_ptr_heads_dev),
          reinterpret_cast<Index**>(indices_ptr_heads_dev),
          reinterpret_cast<int32**>(segids_ptr_heads_dev),
          reinterpret_cast<T**>(outputs_ptr_heads_dev));
}

template <typename T, typename Index>
void SparseSegmentReductionNFunctors<T, Index>::sum_lengths(
    int64 max_seg_lens_size,  // max_output_row_size
    int32 valid_num_columns,
    int64* seg_lens_size_dev,  // output_row_sizes_dev
    int8* seg_lengths_ptr_heads_dev, int64 max_indices_num,
    int64* indices_num_dev, int8* segids_ptr_heads_dev,
    const Eigen::GpuDevice& d) {
  Cuda2DLaunchConfig conf2d =
      GetCuda2DLaunchConfig(max_seg_lens_size, valid_num_columns, d);
  SetToNValue<int32, int64>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, seg_lens_size_dev,
          reinterpret_cast<int32**>(seg_lengths_ptr_heads_dev), int32(0));
  conf2d = GetCuda2DLaunchConfig(max_indices_num, valid_num_columns, d);
  SparseSegmentNLenSumKernel<T, int32>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, indices_num_dev, seg_lens_size_dev,
          reinterpret_cast<int32**>(segids_ptr_heads_dev),
          reinterpret_cast<int32**>(seg_lengths_ptr_heads_dev));
}

#define DEFINE_FUNCTORS(T)                                   \
  template struct SparseSegmentReductionNFunctors<T, int32>; \
  template struct SparseSegmentReductionNFunctors<T, int64>;

TF_CALL_SEGMENT_REDUCTION_TYPES(DEFINE_FUNCTORS);

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
