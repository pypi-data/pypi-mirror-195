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

#ifndef HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_TYPES_H_
#define HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_TYPES_H_

#if HYBRIDBACKEND_TENSORFLOW

#include <tensorflow/core/framework/register_types.h>

namespace tensorflow {

class OpKernelContext;

namespace hybridbackend {

#ifdef HYBRIDBACKEND_TENSORFLOW_HALF
#define TF_CALL_SEGMENT_REDUCTION_TYPES(m)                             \
  TF_CALL_int32(m) TF_CALL_int64(m) TF_CALL_float(m) TF_CALL_double(m) \
      TF_CALL_half(m)
#define TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(m) \
  TF_CALL_float(m) TF_CALL_double(m) TF_CALL_half(m)
#else
#define TF_CALL_SEGMENT_REDUCTION_TYPES(m) \
  TF_CALL_int32(m) TF_CALL_int64(m) TF_CALL_float(m) TF_CALL_double(m)
#define TF_CALL_SEGMENT_REDUCTION_REAL_TYPES(m) \
  TF_CALL_float(m) TF_CALL_double(m)
#endif

#define TF_CALL_SEGMENT_REDUCTION_INDEX_TYPES(m) \
  TF_CALL_int32(m) TF_CALL_int64(m)

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW

#endif  // HYBRIDBACKEND_TENSORFLOW_OPS_SPARSE_SEGMENT_TYPES_H_
