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

#ifndef HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_COMMON_H_
#define HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_COMMON_H_

#if HYBRIDBACKEND_TENSORFLOW

#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/framework/tensor_reference.h>
#include <tensorflow/core/public/version.h>

namespace tensorflow {

class OpKernelContext;

namespace hybridbackend {

Status SparseSegmentReductionNShapeFn(shape_inference::InferenceContext* c);

Status SparseSegmentReductionWithNumSegmentsNShapeFn(
    shape_inference::InferenceContext* c);

Status SparseSegmentReductionGradNShapeFn(shape_inference::InferenceContext* c);

namespace functor {

#if GOOGLE_CUDA

template <typename Index>
struct FindMaxSegId {
  void operator()(OpKernelContext* ctx, const Tensor* seg_ids, Index& max_id);
};

template <typename T, typename Index>
struct SparseSegmentReductionNFunctors {
 public:
  typedef T Type;
  typedef Index IndexType;

  void sum(int64 max_output_total_size, int32 valid_num_columns,
           int64* output_total_sizes_dev, int8* outputs_ptr_heads_dev,
           int64 max_data_sparse_size, int64* data_sparse_sizes_dev,
           int64* data_inner_dims_dev, int8* data_ptr_heads_dev,
           int8* indices_ptr_heads_dev, int8* segids_ptr_heads_dev,
           const Eigen::GpuDevice& d);

  void sum_lengths(int64 max_seg_lens_size, int32 valid_num_columns,
                   int64* seg_lens_size_dev, int8* seg_lengths_ptr_heads_dev,
                   int64 max_indices_num, int64* indices_num_dev,
                   int8* segids_ptr_heads_dev, const Eigen::GpuDevice& d);
};

#endif  // GOOGLE_CUDA

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW

#endif  // HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_COMMON_H_
