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

#ifndef HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_COUNT_NONZERO_H_
#define HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_COUNT_NONZERO_H_

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
template <typename T, typename Tidx, typename Tout>
struct SparseCountNonzeroFunctor {
  void operator()(OpKernelContext* ctx, const Tensor* indices,
                  const Tensor* values, const Tensor* shape, Tensor* output,
                  const int64 axis, const int64 ndims);
};

template <typename T, typename Tidx, typename Tout>
struct SparseCountNonzeroNFunctor {
  void operator()(OpKernelContext* ctx, OpInputList* indices_list,
                  OpInputList* values_list, OpInputList* shapes_list,
                  OpOutputList* outputs, std::vector<int64>& axis_list,
                  std::vector<int64>& ndims_list);
};

#endif  // GOOGLE_CUDA

}  // namespace functor
}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW

#endif  // HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_COUNT_NONZERO_H_
