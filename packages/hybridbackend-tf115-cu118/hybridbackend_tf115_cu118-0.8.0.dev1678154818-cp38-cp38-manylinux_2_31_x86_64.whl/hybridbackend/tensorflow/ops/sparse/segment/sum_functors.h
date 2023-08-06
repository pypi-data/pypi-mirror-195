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

#ifndef HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_SUM_FUNCTORS_H_
#define HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_SUM_FUNCTORS_H_

#if HYBRIDBACKEND_TENSORFLOW

#include <tensorflow/core/framework/op_kernel.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/framework/tensor_reference.h>
#include <tensorflow/core/public/version.h>

namespace tensorflow {

class OpKernelContext;

namespace hybridbackend {
namespace functor {

#if GOOGLE_CUDA

template <typename T, typename Index>
struct SparseSegmentSumNFunctor {
  void operator()(OpKernelContext* ctx, OpInputList* data_list,
                  OpInputList* indices_list, OpInputList* segment_ids_list,
                  OpOutputList* outputs);
};

#endif  // GOOGLE_CUDA

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW

#endif  // HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_SUM_FUNCTORS_H_
