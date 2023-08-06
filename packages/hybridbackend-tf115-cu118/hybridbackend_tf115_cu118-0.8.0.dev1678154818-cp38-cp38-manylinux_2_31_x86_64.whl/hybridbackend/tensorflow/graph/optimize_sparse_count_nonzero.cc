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

#include <tensorflow/core/framework/attr_value_util.h>
#include <tensorflow/core/framework/node_def_util.h>

#include "hybridbackend/common/env.h"
#include "hybridbackend/tensorflow/graph/common/fusion.h"
#include "hybridbackend/tensorflow/graph/common/packing.h"
#include "hybridbackend/tensorflow/graph/op_optimization.h"

namespace tensorflow {
namespace hybridbackend {

namespace {
class SparseCountNonzeroTemplate : public FusionTemplate {
 public:
  SparseCountNonzeroTemplate(bool as_base = false) {
    if (!as_base) {
      const fusion_template::NodeDesc n0 = {
          .key = "SparseToDense",
          .op = "SparseToDense",
          .inputs = {"0", "1", "2", "3"},
          .outputs = {{"count_nonzero_NotEqual"}}};
      temp_nodes_.emplace_back(n0);

      const fusion_template::NodeDesc n1 = {
          .key = "count_nonzero_zeros",
          .op = "Const",
          .inputs = {},
          .outputs = {{"count_nonzero_NotEqual"}}};
      temp_nodes_.emplace_back(n1);

      const fusion_template::NodeDesc n2 = {
          .key = "count_nonzero_NotEqual",
          .op = "NotEqual",
          .inputs = {"SparseToDense", "count_nonzero_zeros"},
          .outputs = {{"count_nonzero_Cast"}}};
      temp_nodes_.emplace_back(n2);

      const fusion_template::NodeDesc n3 = {
          .key = "count_nonzero_Cast",
          .op = "Cast",
          .inputs = {"count_nonzero_NotEqual"},
          .outputs = {{"count_nonzero_Sum"}}};
      temp_nodes_.emplace_back(n3);

      const fusion_template::NodeDesc n4 = {
          .key = "count_nonzero_Sum_reduction_indices",
          .op = "Const",
          .inputs = {},
          .outputs = {{"count_nonzero_Sum"}}};
      temp_nodes_.emplace_back(n4);

      const fusion_template::NodeDesc n5 = {
          .key = "count_nonzero_Sum",
          .op = "Sum",
          .inputs = {"count_nonzero_Cast",
                     "count_nonzero_Sum_reduction_indices"},
          .outputs = {{"0"}}};
      temp_nodes_.emplace_back(n5);

      first_key_ = "SparseToDense";
      num_inputs_ = 4;
      num_outputs_ = 1;
      fused_op_input_idx_.emplace_back(0);
      fused_op_input_idx_.emplace_back(2);
      fused_op_input_idx_.emplace_back(1);
      fused_op_output_idx_.emplace_back(0);
    }
  }

  const string Name() override { return "SparseCountNonzeroTemplate"; }

  bool AddSubgraph(std::map<std::string, fusion_template::NodeMatching>& nodes,
                   std::string name_postfix, Graph* g,
                   std::vector<const Edge*>& inputs,
                   std::vector<std::vector<const Edge*>>& outputs) override {
    NodeDef fused_def;
    fused_def.set_op("HbSparseCountNonzero");
    fused_def.set_name(+"hb_sparse_count_nonzero" + name_postfix);
    auto origin_device = inputs[0]->dst()->def().device();
    fused_def.set_device(origin_device);
    auto sp_to_dense_op_attr = nodes["SparseToDense"].node->def().attr();
    auto count_nonzero_sum_attr = nodes["count_nonzero_Sum"].node->def().attr();
    auto axis_value_from_sum =
        nodes["count_nonzero_Sum_reduction_indices"].node->def().attr();

    fused_def.mutable_attr()->insert({"T", sp_to_dense_op_attr.at("T")});
    fused_def.mutable_attr()->insert(
        {"Tidx", sp_to_dense_op_attr.at("Tindices")});
    fused_def.mutable_attr()->insert({"Tout", count_nonzero_sum_attr.at("T")});

    AttrValue axis_attr;
    Tensor axis_val(axis_value_from_sum.at("value").tensor().dtype());
    CHECK(axis_val.FromProto(axis_value_from_sum.at("value").tensor()));

    SetAttrValue(int(axis_val.flat<int>()(0)), &axis_attr);
    fused_def.mutable_attr()->insert({"axis", axis_attr});

    AddInput(fused_def, inputs[fused_op_input_idx_[0]]);
    AddInput(fused_def, inputs[fused_op_input_idx_[1]]);
    AddInput(fused_def, inputs[fused_op_input_idx_[2]]);

    Status status;
    Node* fused_node = g->AddNode(fused_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }

    AddInputEdge(g, fused_node, 0, inputs[fused_op_input_idx_[0]]);
    AddInputEdge(g, fused_node, 1, inputs[fused_op_input_idx_[1]]);
    AddInputEdge(g, fused_node, 2, inputs[fused_op_input_idx_[2]]);

    AddOutputEdges(g, fused_node, 0, outputs[fused_op_output_idx_[0]]);
    return true;
  }

  bool AddSubgraph(std::map<std::string, fusion_template::NodeMatching>& nodes,
                   std::string name_prefix, Graph* g,
                   std::vector<const Edge*>& inputs,
                   std::vector<const Edge*>& deps_inputs,
                   std::vector<std::vector<const Edge*>>& outputs) override {
    LOG(ERROR) << "Not implemented in SparseCountNonzeroTemplate";
    return false;
  }

  bool CheckDynamicInputs(
      const Node* node, const fusion_template::NodeDesc* temp_node,
      const int dy_mode, std::vector<const Edge*>& fused_op_inputs,
      std::map<const std::string, fusion_template::NodeDesc>& temp_node_map,
      std::map<std::string, fusion_template::NodeMatching>& matched_node_map)
      override {
    LOG(ERROR) << "Not implemented in SparseCountNonzeroTemplate";
    return false;
  }

  bool CheckDynamicOutputs(
      const Node* node, const fusion_template::NodeDesc* temp_node,
      const int dy_mode,
      std::vector<std::vector<const Edge*>>& fused_op_outputs,
      std::map<const std::string, fusion_template::NodeDesc>& temp_node_map,
      std::map<std::string, fusion_template::NodeMatching>& matched_node_map)
      override {
    LOG(ERROR) << "Not implemented in SparseCountNonzeroTemplate";
    return false;
  }
};

class SparseReorderAndCountNonzeroTemplate : public SparseCountNonzeroTemplate {
 public:
  SparseReorderAndCountNonzeroTemplate() : SparseCountNonzeroTemplate(true) {
    const fusion_template::NodeDesc n0 = {
        .key = "SparseReorder",
        .op = "SparseReorder",
        .inputs = {"0", "1", "2"},
        .outputs = {{"SparseToDense"}, {"SparseToDense"}}};
    temp_nodes_.emplace_back(n0);

    const fusion_template::NodeDesc n1 = {.key = "SparseTensor_dense_shape",
                                          .op = "Const",
                                          .inputs = {},
                                          .outputs = {{"SparseToDense"}}};
    temp_nodes_.emplace_back(n1);

    const fusion_template::NodeDesc n2 = {.key = "zeros",
                                          .op = "Const",
                                          .inputs = {},
                                          .outputs = {{"SparseToDense"}}};
    temp_nodes_.emplace_back(n2);

    const fusion_template::NodeDesc n3 = {
        .key = "SparseToDense",
        .op = "SparseToDense",
        .inputs = {"SparseReorder", "SparseTensor_dense_shape", "SparseReorder",
                   "zeros"},
        .outputs = {{"count_nonzero_NotEqual"}}};
    temp_nodes_.emplace_back(n3);

    const fusion_template::NodeDesc n4 = {
        .key = "count_nonzero_zeros",
        .op = "Const",
        .inputs = {},
        .outputs = {{"count_nonzero_NotEqual"}}};
    temp_nodes_.emplace_back(n4);

    const fusion_template::NodeDesc n5 = {
        .key = "count_nonzero_NotEqual",
        .op = "NotEqual",
        .inputs = {"SparseToDense", "count_nonzero_zeros"},
        .outputs = {{"count_nonzero_Cast"}}};
    temp_nodes_.emplace_back(n5);

    const fusion_template::NodeDesc n6 = {.key = "count_nonzero_Cast",
                                          .op = "Cast",
                                          .inputs = {"count_nonzero_NotEqual"},
                                          .outputs = {{"count_nonzero_Sum"}}};
    temp_nodes_.emplace_back(n6);

    const fusion_template::NodeDesc n7 = {
        .key = "count_nonzero_Sum_reduction_indices",
        .op = "Const",
        .inputs = {},
        .outputs = {{"count_nonzero_Sum"}}};
    temp_nodes_.emplace_back(n7);

    const fusion_template::NodeDesc n8 = {
        .key = "count_nonzero_Sum",
        .op = "Sum",
        .inputs = {"count_nonzero_Cast", "count_nonzero_Sum_reduction_indices"},
        .outputs = {{"0"}}};
    temp_nodes_.emplace_back(n8);

    first_key_ = "SparseToDense";
    num_inputs_ = 3;
    num_outputs_ = 1;
    fused_op_input_idx_.emplace_back(0);
    fused_op_input_idx_.emplace_back(1);
    fused_op_input_idx_.emplace_back(2);
    fused_op_output_idx_.emplace_back(0);
  }

  const string Name() override {
    return "SparseReorderAndCountNonzeroTemplate";
  }
};

inline bool CountNonzeroOptimizationDisabled() {
  static const bool kCountNonzeroOptimizationDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_COUNT_NONZERO_OPTIMIZATION_DISABLED", false);
  return kCountNonzeroOptimizationDisabled;
}

inline bool CountNonzeroPackingDisabled() {
  static const bool kCountNonzeroPackingDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_COUNT_NONZERO_PACKING_DISABLED", false);
  return kCountNonzeroPackingDisabled;
}
}  // namespace

class OptimizeSparseCountNonzeroReductionPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_FALSE(disabled || CountNonzeroOptimizationDisabled())) {
      return Status::OK();
    }

    SparseReorderAndCountNonzeroTemplate count_nonzero;
    Fuse(graph, count_nonzero);
    SparseCountNonzeroTemplate count_nonzero_with_reorder;
    Fuse(graph, count_nonzero_with_reorder);

    if (TF_PREDICT_TRUE(!CountNonzeroPackingDisabled())) {
      TF_RETURN_IF_ERROR(
          Pack("HbSparseCountNonzero", "HbSparseCountNonzeroN")
              .WithTypeAttr(
                  "T", {DT_INT64, DT_INT32, DT_INT16, DT_INT8, DT_UINT16,
                        DT_UINT8, DT_FLOAT, DT_DOUBLE, DT_HALF, DT_BFLOAT16})
              .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
              .WithTypeAttr("Tout", {DT_INT64, DT_INT32})
              .WithIntAttr("axis")
              .In(graph));
    }
    return Status::OK();
  }
};

REGISTER_REDUCTION_OPTIMIZATION(OptimizeSparseCountNonzeroReductionPass);

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
