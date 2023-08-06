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
#include "hybridbackend/tensorflow/ops/sparse/count_nonzero/functors.h"

namespace tensorflow {
namespace hybridbackend {

using GPUDevice = Eigen::GpuDevice;

template <typename T, typename Tidx, typename Tout>
__global__ void SparseCountNonzeroKernel(const Tidx* indices, const T* values,
                                         const int64* shape, Tout* output,
                                         const int64 num_ids, const int axis,
                                         const int ndims) {
  for (int64 input_index : CudaGridRangeX(num_ids)) {
    const int64 coord_offset = input_index * ndims;
    if (ldg(values + input_index) != T(0)) {
      int64 output_offset = 0;
      // obtain the output offset
      for (int i = 0; i < axis - 1; i++) {
        output_offset +=
            shape[i + 1] * static_cast<int64>(ldg(indices + coord_offset + i));
      }
      // process the last one
      output_offset +=
          static_cast<int64>(ldg(indices + coord_offset + axis - 1));
      // write counts to output
      CudaAtomicAdd(output + output_offset, Tout(1));
    }
  }
}

template <typename T, typename Tidx, typename Tout>
__global__ void SparseCountNonzeroNKernel(const Cuda2DLaunchConfig config,
                                          int64* axis, int64* ndims,
                                          int64* num_ids, Tidx** indices,
                                          T** values, int64** shapes,
                                          Tout** outputs) {
  CUDA_AXIS_KERNEL_LOOP(g_idx, config.virtual_thread_count.y, Y) {
    CUDA_AXIS_KERNEL_LOOP(g_offset, config.virtual_thread_count.x, X) {
      if (g_offset < num_ids[g_idx]) {
        const int64 coord_offset = g_offset * ndims[g_idx];
        if (ldg(values[g_idx] + g_offset) != T(0)) {
          int64 output_offset = 0;
          int64 axis_g = axis[g_idx];
          int64* shapes_g = shapes[g_idx];
          Tidx* indices_g = indices[g_idx];
          for (int i = 0; i < axis_g - 1; i++) {
            output_offset +=
                shapes_g[i + 1] *
                static_cast<int64>(ldg(indices_g + coord_offset + i));
          }
          // process the last one
          output_offset +=
              static_cast<int64>(ldg(indices_g + coord_offset + axis_g - 1));
          // write counts to output
          CudaAtomicAdd(outputs[g_idx] + output_offset, Tout(1));
        }
      }
    }
  }
}

namespace functor {

template <typename T, typename Tidx, typename Tout>
void SparseCountNonzeroFunctor<T, Tidx, Tout>::operator()(
    OpKernelContext* ctx, const Tensor* indices, const Tensor* values,
    const Tensor* shape, Tensor* output, const int64 axis, const int64 ndims) {
  auto* stream = ctx->op_device_context()->stream();

  // copy shape from host to device
  Tensor shape_on_device;
  ctx->allocate_temp(shape->dtype(), TensorShape{shape->NumElements()},
                     &shape_on_device);
  if (!ctx->status().ok()) {
    return;
  }
  // copy data
  se::DeviceMemoryBase dst_ptr(
      const_cast<char*>(shape_on_device.tensor_data().data()),
      shape_on_device.TotalBytes());
  stream->ThenMemcpy(&dst_ptr, shape->tensor_data().data(),
                     shape->TotalBytes());
  stream->BlockHostUntilDone();

  const int64 num_ids = indices->NumElements() / ndims;
  if (num_ids == 0) {
    return;
  }
  Tout* d_output = output->flat<Tout>().data();
  const GPUDevice d = ctx->eigen_device<GPUDevice>();

  // initialize output counts to 0
  se::DeviceMemoryBase output_mem(d_output, output->TotalBytes());
  stream->ThenMemZero(&output_mem, output->NumElements() * sizeof(Tout));

  // count non zeros
  CudaLaunch(SparseCountNonzeroKernel<T, Tidx, Tout>, num_ids, 0, d, nullptr,
             indices->flat<Tidx>().data(), values->flat<T>().data(),
             shape_on_device.flat<int64>().data(), d_output, num_ids, axis,
             ndims);
}

#define DEFINE_SPARSE_COUNT_NONZERO(T, Tidx, Tout) \
  template struct SparseCountNonzeroFunctor<T, Tidx, Tout>

#define DEFINE_SPARSE_COUNT_NONZERO_OPS(T)      \
  DEFINE_SPARSE_COUNT_NONZERO(T, int32, int32); \
  DEFINE_SPARSE_COUNT_NONZERO(T, int64, int32); \
  DEFINE_SPARSE_COUNT_NONZERO(T, int32, int64); \
  DEFINE_SPARSE_COUNT_NONZERO(T, int64, int64);

TF_CALL_REAL_NUMBER_TYPES(DEFINE_SPARSE_COUNT_NONZERO_OPS);

template <typename T, typename Tidx, typename Tout>
void SparseCountNonzeroNFunctor<T, Tidx, Tout>::operator()(
    OpKernelContext* ctx, OpInputList* indices_list, OpInputList* values_list,
    OpInputList* shapes_list, OpOutputList* outputs, std::vector<int64>& axis,
    std::vector<int64>& ndims) {
  auto* stream = ctx->op_device_context()->stream();
  const GPUDevice d = ctx->eigen_device<GPUDevice>();

  const int32 num_columns = indices_list->size();
  std::vector<int> valid_column_id;
  for (int i = 0; i < num_columns; ++i) {
    if (((*indices_list)[i].NumElements() / ndims[i]) > 0 &&
        (*outputs)[i]->NumElements() > 0) {
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

  // prepare ptr heads
  const int64 ptr_heads_bytes = 4 * valid_num_columns * sizeof(T*);
  Tensor ptr_heads;
  ctx->allocate_temp(DT_INT8, TensorShape{ptr_heads_bytes}, &ptr_heads,
                     host_alloc_attr);
  Tensor ptr_heads_dev;
  ctx->allocate_temp(DT_INT8, TensorShape{ptr_heads_bytes}, &ptr_heads_dev);

  int8* indices_ptr_heads = ptr_heads.flat<int8>().data();
  int8* indices_ptr_heads_dev = ptr_heads_dev.flat<int8>().data();

  int8* values_ptr_heads =
      ptr_heads.flat<int8>().data() + valid_num_columns * sizeof(T*);
  int8* values_ptr_heads_dev =
      ptr_heads_dev.flat<int8>().data() + valid_num_columns * sizeof(T*);

  int8* shapes_ptr_heads =
      ptr_heads.flat<int8>().data() + 2 * valid_num_columns * sizeof(T*);
  int8* shapes_ptr_heads_dev =
      ptr_heads_dev.flat<int8>().data() + 2 * valid_num_columns * sizeof(T*);

  int8* outputs_ptr_heads =
      ptr_heads.flat<int8>().data() + 3 * valid_num_columns * sizeof(T*);
  int8* outputs_ptr_heads_dev =
      ptr_heads_dev.flat<int8>().data() + 3 * valid_num_columns * sizeof(T*);

  std::vector<const Tensor*> indices_list_vec;
  std::vector<const Tensor*> values_list_vec;
  std::vector<const Tensor*> shapes_list_vec;
  std::vector<const Tensor*> outputs_vec;

  for (int i = 0; i < valid_num_columns; ++i) {
    indices_list_vec.emplace_back(&((*indices_list)[valid_column_id[i]]));
    values_list_vec.emplace_back(&((*values_list)[valid_column_id[i]]));
    shapes_list_vec.emplace_back(&((*shapes_list)[valid_column_id[i]]));
    outputs_vec.emplace_back((*outputs)[valid_column_id[i]]);
  }

  functor::CopyPtrsNFunctor<Tidx> copy_indices_ptr;
  functor::CopyPtrsNFunctor<T> copy_values_ptr;
  functor::CopyPtrsNFunctor<int64> copy_shapes_ptr;
  functor::CopyPtrsNFunctor<Tout> copy_outputs_ptr;

  copy_indices_ptr(ctx, indices_ptr_heads, indices_ptr_heads_dev,
                   &indices_list_vec, valid_num_columns);
  copy_values_ptr(ctx, values_ptr_heads, values_ptr_heads_dev, &values_list_vec,
                  valid_num_columns);
  copy_shapes_ptr(ctx, shapes_ptr_heads, shapes_ptr_heads_dev, &shapes_list_vec,
                  valid_num_columns);
  copy_outputs_ptr(ctx, outputs_ptr_heads, outputs_ptr_heads_dev, &outputs_vec,
                   valid_num_columns);

  const int64 sizes_length = 4 * valid_num_columns;
  Tensor sizes;
  ctx->allocate_temp(DT_INT64, TensorShape{sizes_length}, &sizes,
                     host_alloc_attr);
  Tensor sizes_dev;
  ctx->allocate_temp(DT_INT64, TensorShape{sizes_length}, &sizes_dev);

  int64* axis_list = sizes.flat<int64>().data();
  int64* axis_list_dev = sizes_dev.flat<int64>().data();

  int64* ndims_list = sizes.flat<int64>().data() + valid_num_columns;
  int64* ndims_list_dev = sizes_dev.flat<int64>().data() + valid_num_columns;

  int64* num_ids_list = sizes.flat<int64>().data() + 2 * valid_num_columns;
  int64* num_ids_list_dev =
      sizes_dev.flat<int64>().data() + 2 * valid_num_columns;
  int64* output_total_sizes =
      sizes.flat<int64>().data() + 3 * valid_num_columns;
  int64* output_total_sizes_dev =
      sizes_dev.flat<int64>().data() + 3 * valid_num_columns;

  for (int i = 0; i < valid_num_columns; ++i) {
    axis_list[i] = axis[valid_column_id[i]];
    ndims_list[i] = ndims[valid_column_id[i]];
    num_ids_list[i] = (*indices_list)[valid_column_id[i]].NumElements() /
                      ndims[valid_column_id[i]];
    output_total_sizes[i] = (*outputs)[valid_column_id[i]]->NumElements();
  }

  functor::CopySizesNFunctor<int64> copy_sizes_n;
  copy_sizes_n(ctx, axis_list, axis_list_dev, valid_num_columns);
  copy_sizes_n(ctx, ndims_list, ndims_list_dev, valid_num_columns);
  copy_sizes_n(ctx, num_ids_list, num_ids_list_dev, valid_num_columns);
  copy_sizes_n(ctx, output_total_sizes, output_total_sizes_dev,
               valid_num_columns);

  int64 max_output_total_size = *std::max_element(
      output_total_sizes, output_total_sizes + valid_num_columns);
  int64 max_num_ids_list =
      *std::max_element(num_ids_list, num_ids_list + valid_num_columns);

  Cuda2DLaunchConfig conf2d =
      GetCuda2DLaunchConfig(max_output_total_size, valid_num_columns, d);
  SetToNValue<Tout, int64>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, output_total_sizes_dev,
          reinterpret_cast<Tout**>(outputs_ptr_heads_dev), Tout(0));

  conf2d = GetCuda2DLaunchConfig(max_num_ids_list, valid_num_columns, d);
  SparseCountNonzeroNKernel<T, Tidx, Tout>
      <<<conf2d.block_count, conf2d.thread_per_block, 0, d.stream()>>>(
          conf2d, axis_list_dev, ndims_list_dev, num_ids_list_dev,
          reinterpret_cast<Tidx**>(indices_ptr_heads_dev),
          reinterpret_cast<T**>(values_ptr_heads_dev),
          reinterpret_cast<int64**>(shapes_ptr_heads_dev),
          reinterpret_cast<Tout**>(outputs_ptr_heads_dev));
}

#define DEFINE_SPARSE_COUNT_NONZERO_N(T, Tidx, Tout) \
  template struct SparseCountNonzeroNFunctor<T, Tidx, Tout>

#define DEFINE_SPARSE_COUNT_NONZERO_N_OPS(T)      \
  DEFINE_SPARSE_COUNT_NONZERO_N(T, int32, int32); \
  DEFINE_SPARSE_COUNT_NONZERO_N(T, int64, int32); \
  DEFINE_SPARSE_COUNT_NONZERO_N(T, int32, int64); \
  DEFINE_SPARSE_COUNT_NONZERO_N(T, int64, int64);

TF_CALL_REAL_NUMBER_TYPES(DEFINE_SPARSE_COUNT_NONZERO_N_OPS);

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // GOOGLE_CUDA
#endif  // HYBRIDBACKEND_TENSORFLOW
