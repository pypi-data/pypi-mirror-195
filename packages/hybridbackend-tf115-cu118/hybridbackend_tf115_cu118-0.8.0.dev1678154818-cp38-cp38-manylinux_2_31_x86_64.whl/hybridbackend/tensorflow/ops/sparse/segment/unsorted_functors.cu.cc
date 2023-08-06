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

#include <tensorflow/core/framework/register_types.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/public/version.h>

#include "hybridbackend/common/atomic.cu.h"
#include "hybridbackend/tensorflow/common/device_functions.h"
#include "hybridbackend/tensorflow/common/fusion_helper.cu.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/types.h"
#include "hybridbackend/tensorflow/ops/sparse/segment/unsorted_functors.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

template <typename T, typename Index>
__global__ void UnsortedSegmentSumNKernel(const Cuda2DLaunchConfig config,
                                          int64* data_total_size,
                                          int64* output_total_size,
                                          int64* data_inner_dim, T** data,
                                          Index** seg_ids, T** output) {
  CUDA_AXIS_KERNEL_LOOP(g_idx, config.virtual_thread_count.y, Y) {
    CUDA_AXIS_KERNEL_LOOP(g_offset, config.virtual_thread_count.x, X) {
      if (g_offset < data_total_size[g_idx]) {
        const int64 data_inner_dim_thd = data_inner_dim[g_idx];
        const int64 data_row = g_offset / data_inner_dim_thd;
        const int64 data_offset = g_offset % data_inner_dim_thd;
        const Index output_row = seg_ids[g_idx][data_row];
        const int64 output_idx = output_row * data_inner_dim_thd + data_offset;
        if (output_idx < 0 || output_idx >= output_total_size[g_idx]) {
          continue;
        }
        CudaAtomicAdd(output[g_idx] + output_idx, ldg(data[g_idx] + g_offset));
      }
    }
  }
}

namespace functor {

template <typename T, typename Index>
void UnsortedSegmentReductionNFunctor<T, Index>::operator()(
    OpKernelContext* ctx, OpInputList* data_list, OpInputList* segment_ids_list,
    OpOutputList* outputs) {
  const GPUDevice d = ctx->eigen_device<GPUDevice>();
  const int32 num_columns = data_list->size();
  std::vector<int> valid_column_id;
  for (int i = 0; i < num_columns; ++i) {
    if ((*data_list)[i].NumElements() > 0 && (*outputs)[i]->NumElements() > 0) {
      valid_column_id.emplace_back(i);
    }
  }
  const int32 valid_num_columns = valid_column_id.size();
  if (valid_num_columns == 0) {
    return;
  }

  AllocatorAttributes host_alloc_attr;
  host_alloc_attr.set_on_host(true);
  host_alloc_attr.set_gpu_compatible(true);

  const int64 ptr_heads_bytes = 3 * valid_num_columns * sizeof(T*);
  Tensor ptr_heads;
  ctx->allocate_temp(DT_INT8, TensorShape{ptr_heads_bytes}, &ptr_heads,
                     host_alloc_attr);
  Tensor ptr_heads_dev;
  ctx->allocate_temp(DT_INT8, TensorShape{ptr_heads_bytes}, &ptr_heads_dev);

  int8* data_ptr_heads = ptr_heads.flat<int8>().data();
  int8* data_ptr_heads_dev = ptr_heads_dev.flat<int8>().data();

  int8* segids_ptr_heads =
      ptr_heads.flat<int8>().data() + valid_num_columns * sizeof(int32*);
  int8* segids_ptr_heads_dev =
      ptr_heads_dev.flat<int8>().data() + valid_num_columns * sizeof(int32*);

  int8* outputs_ptr_heads =
      ptr_heads.flat<int8>().data() + 2 * valid_num_columns * sizeof(T*);
  int8* outputs_ptr_heads_dev =
      ptr_heads_dev.flat<int8>().data() + 2 * valid_num_columns * sizeof(T*);

  std::vector<const Tensor*> data_list_vec;
  std::vector<const Tensor*> segment_ids_list_vec;
  std::vector<const Tensor*> outputs_vec;
  for (int i = 0; i < valid_num_columns; ++i) {
    data_list_vec.emplace_back(&((*data_list)[valid_column_id[i]]));
    segment_ids_list_vec.emplace_back(
        &((*segment_ids_list)[valid_column_id[i]]));
    outputs_vec.emplace_back((*outputs)[valid_column_id[i]]);
  }

  functor::CopyPtrsNFunctor<T> prep_data_functor;
  prep_data_functor(ctx, data_ptr_heads, data_ptr_heads_dev, &data_list_vec,
                    valid_num_columns);
  prep_data_functor(ctx, outputs_ptr_heads, outputs_ptr_heads_dev, &outputs_vec,
                    valid_num_columns);

  functor::CopyPtrsNFunctor<Index> prep_segids_functor;
  prep_segids_functor(ctx, segids_ptr_heads, segids_ptr_heads_dev,
                      &segment_ids_list_vec, valid_num_columns);

  const int64 sizes_length = 3 * valid_num_columns;
  Tensor sizes;
  ctx->allocate_temp(DT_INT64, TensorShape{sizes_length}, &sizes,
                     host_alloc_attr);
  Tensor sizes_dev;
  ctx->allocate_temp(DT_INT64, TensorShape{sizes_length}, &sizes_dev);

  int64* data_inner_dims = sizes.flat<int64>().data();
  int64* data_inner_dims_dev = sizes_dev.flat<int64>().data();

  int64* data_total_sizes = sizes.flat<int64>().data() + valid_num_columns;
  int64* data_total_sizes_dev =
      sizes_dev.flat<int64>().data() + valid_num_columns;

  int64* output_total_sizes =
      sizes.flat<int64>().data() + 2 * valid_num_columns;
  int64* output_total_sizes_dev =
      sizes_dev.flat<int64>().data() + 2 * valid_num_columns;

  for (int i = 0; i < valid_num_columns; ++i) {
    data_inner_dims[i] =
        (*data_list)[valid_column_id[i]].flat_outer_dims<T>().dimension(1);
    data_total_sizes[i] = (*data_list)[valid_column_id[i]].NumElements();
    output_total_sizes[i] = (*outputs)[valid_column_id[i]]->NumElements();
  }

  int64 max_output_total_size = *std::max_element(
      output_total_sizes, output_total_sizes + valid_num_columns);

  int64 max_data_total_size =
      *std::max_element(data_total_sizes, data_total_sizes + valid_num_columns);

  functor::CopySizesNFunctor<int64> copy_sizes_n;
  copy_sizes_n(ctx, data_inner_dims, data_inner_dims_dev, valid_num_columns);
  copy_sizes_n(ctx, data_total_sizes, data_total_sizes_dev, valid_num_columns);
  copy_sizes_n(ctx, output_total_sizes, output_total_sizes_dev,
               valid_num_columns);

  // initialize output by default value
  Cuda2DLaunchConfig conf2d =
      GetCuda2DLaunchConfig(max_output_total_size, valid_num_columns, d);
  SetToNValue<T, int64>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, output_total_sizes_dev,
          reinterpret_cast<T**>(outputs_ptr_heads_dev), T(0.0));
  conf2d = GetCuda2DLaunchConfig(max_data_total_size, valid_num_columns, d);
  // launch a kernel
  UnsortedSegmentSumNKernel<T, Index>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, data_total_sizes_dev, output_total_sizes_dev,
          data_inner_dims_dev, reinterpret_cast<T**>(data_ptr_heads_dev),
          reinterpret_cast<Index**>(segids_ptr_heads_dev),
          reinterpret_cast<T**>(outputs_ptr_heads_dev));
}

#define DEFINE_UNSORTED_SEGMENT_REDUCTION_N(T, Index) \
  template struct UnsortedSegmentReductionNFunctor<T, Index>

#define DEFINE_UNSORTED_SEGMENT_REDUCTION_OPS(T) \
  DEFINE_UNSORTED_SEGMENT_REDUCTION_N(T, int32); \
  DEFINE_UNSORTED_SEGMENT_REDUCTION_N(T, int64);

TF_CALL_SEGMENT_REDUCTION_TYPES(DEFINE_UNSORTED_SEGMENT_REDUCTION_OPS);

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
