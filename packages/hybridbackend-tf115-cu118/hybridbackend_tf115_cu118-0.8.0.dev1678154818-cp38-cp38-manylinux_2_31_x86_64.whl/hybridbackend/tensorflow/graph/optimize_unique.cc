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

#include <vector>

#include "hybridbackend/common/env.h"
#include "hybridbackend/tensorflow/graph/common/packing.h"
#include "hybridbackend/tensorflow/graph/common/relocation.h"
#include "hybridbackend/tensorflow/graph/common/replacing.h"
#include "hybridbackend/tensorflow/graph/op_optimization.h"

namespace tensorflow {
namespace hybridbackend {

namespace {
inline bool UniqueOptimizationDisabled() {
  static const bool kUniqueOptimizationDisabled =
      ::hybridbackend::EnvVarGetBool("HB_OP_UNIQUE_OPTIMIZATION_DISABLED",
                                     false);
  return kUniqueOptimizationDisabled;
}

inline bool UniqueRelocationDisabled() {
  static const bool kUniqueRelocationDisabled =
      ::hybridbackend::EnvVarGetBool("HB_OP_UNIQUE_RELOCATION_DISABLED", false);
  return kUniqueRelocationDisabled;
}

inline bool UniquePackingDisabled() {
  static const bool kUniquePackingDisabled =
      ::hybridbackend::EnvVarGetBool("HB_OP_UNIQUE_PACKING_DISABLED", false);
  return kUniquePackingDisabled;
}

}  // namespace

class OptimizeUniqueReplacingPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_FALSE(disabled || UniqueOptimizationDisabled())) {
      return Status::OK();
    }

    if (TF_PREDICT_TRUE(!UniqueRelocationDisabled())) {
      Relocate("Unique").WithInput(0).In(graph);
    }

    TF_RETURN_IF_ERROR(
        Replace("Unique", "HbUniqueByHash")
            .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_UINT64, DT_UINT32})
            .WithTypeAttr("out_idx", {DT_INT64, DT_INT32})
            .In(graph));

    return Status::OK();
  }
};

REGISTER_REPLACING_OPTIMIZATION(OptimizeUniqueReplacingPass);

class OptimizeUniqueReductionPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_FALSE(disabled || UniqueOptimizationDisabled())) {
      return Status::OK();
    }

    if (TF_PREDICT_TRUE(!UniquePackingDisabled())) {
      TF_RETURN_IF_ERROR(
          Pack("HbUniqueByHash", "HbUniqueNByHash")
              .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_UINT64, DT_UINT32})
              .WithTypeAttr("out_idx", {DT_INT64, DT_INT32})
              .In(graph));
    }
    return Status::OK();
  }
};

REGISTER_REDUCTION_OPTIMIZATION(OptimizeUniqueReductionPass);

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
