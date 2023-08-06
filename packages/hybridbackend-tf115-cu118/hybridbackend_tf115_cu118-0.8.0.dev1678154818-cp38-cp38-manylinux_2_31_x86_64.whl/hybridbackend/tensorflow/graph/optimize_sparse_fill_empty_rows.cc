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

inline bool SparseFillEmptyRowsOptimizationDisabled() {
  static const bool kSparseFillEmptyRowsOptimizationDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_FILL_EMPTY_ROWS_OPTIMIZATION_DISABLED", true);
  return kSparseFillEmptyRowsOptimizationDisabled;
}

inline bool SparseFillEmptyRowsPackingDisabled() {
  static const bool kSparseFillEmptyRowsPackingDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_FILL_EMPTY_ROWS_PACKING_DISABLED", true);
  return kSparseFillEmptyRowsPackingDisabled;
}
}  // namespace

class OptimizeSparseFillEmptyRowsReplacingPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_TRUE(disabled ||
                        SparseFillEmptyRowsOptimizationDisabled())) {
      return Status::OK();
    }

    TF_RETURN_IF_ERROR(Replace("SparseFillEmptyRows", "HbSparseFillEmptyRows")
                           .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_UINT64,
                                               DT_UINT32, DT_FLOAT})
                           .In(graph));
    return Status::OK();
  }
};

REGISTER_REPLACING_OPTIMIZATION(OptimizeSparseFillEmptyRowsReplacingPass);

class OptimizeSparseFillEmptyRowsReductionPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_TRUE(disabled ||
                        SparseFillEmptyRowsOptimizationDisabled())) {
      return Status::OK();
    }

    if (TF_PREDICT_TRUE(!SparseFillEmptyRowsPackingDisabled())) {
      TF_RETURN_IF_ERROR(Pack("HbSparseFillEmptyRows", "HbSparseFillEmptyRowsN")
                             .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_UINT64,
                                                 DT_UINT32, DT_FLOAT})
                             .In(graph));
    }
    return Status::OK();
  }
};

REGISTER_REDUCTION_OPTIMIZATION(OptimizeSparseFillEmptyRowsReductionPass);

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
