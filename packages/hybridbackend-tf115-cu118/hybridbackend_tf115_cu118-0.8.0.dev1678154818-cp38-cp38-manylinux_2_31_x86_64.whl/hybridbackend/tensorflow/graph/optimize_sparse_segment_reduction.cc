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

#include <absl/strings/str_cat.h>
#include <vector>

#include "hybridbackend/common/env.h"
#include "hybridbackend/tensorflow/graph/common/fusion.h"
#include "hybridbackend/tensorflow/graph/common/packing.h"
#include "hybridbackend/tensorflow/graph/common/pruning.h"
#include "hybridbackend/tensorflow/graph/common/relocation.h"
#include "hybridbackend/tensorflow/graph/common/replacing.h"
#include "hybridbackend/tensorflow/graph/op_optimization.h"

namespace tensorflow {
namespace hybridbackend {

namespace {
class ArgSortAndSparseSegmentReductionFusionTemplate : public FusionTemplate {
 public:
  ArgSortAndSparseSegmentReductionFusionTemplate(bool as_base = false) {
    if (!as_base) {
      const fusion_template::NodeDesc n0 = {.key = "argsort_neg",
                                            .op = "Neg",
                                            .inputs = {"0"},
                                            .outputs = {{"argsort_topkv2"}}};
      temp_nodes_.emplace_back(n0);

      const fusion_template::NodeDesc n1 = {
          .key = "argsort_shape",
          .op = "Const",
          .inputs = {},
          .outputs = {{"argsort_strided_slice"}}};
      temp_nodes_.emplace_back(n1);

      const fusion_template::NodeDesc n2 = {
          .key = "argsort_strided_slice_stack",
          .op = "Const",
          .inputs = {},
          .outputs = {{"argsort_strided_slice"}}};
      temp_nodes_.emplace_back(n2);

      const fusion_template::NodeDesc n3 = {
          .key = "argsort_strided_slice_stack_1",
          .op = "Const",
          .inputs = {},
          .outputs = {{"argsort_strided_slice"}}};
      temp_nodes_.emplace_back(n3);

      const fusion_template::NodeDesc n4 = {
          .key = "argsort_strided_slice_stack_2",
          .op = "Const",
          .inputs = {},
          .outputs = {{"argsort_strided_slice"}}};
      temp_nodes_.emplace_back(n4);

      const fusion_template::NodeDesc n5 = {
          .key = "argsort_strided_slice",
          .op = "StridedSlice",
          .inputs = {"argsort_shape", "argsort_strided_slice_stack",
                     "argsort_strided_slice_stack_1",
                     "argsort_strided_slice_stack_2"},
          .outputs = {{"argsort_topkv2"}}};
      temp_nodes_.emplace_back(n5);

      const fusion_template::NodeDesc n6 = {
          .key = "argsort_topkv2",
          .op = "TopKV2",
          .inputs = {"argsort_neg", "argsort_strided_slice"},
          .outputs = {{}, {"sparse_segment_sum_with_num_segments", "0"}}};
      temp_nodes_.emplace_back(n6);

      const fusion_template::NodeDesc n7 = {.key = "sort_neg",
                                            .op = "Neg",
                                            .inputs = {"0"},
                                            .outputs = {{"sort_topkv2"}}};
      temp_nodes_.emplace_back(n7);

      const fusion_template::NodeDesc n8 = {
          .key = "sort_shape",
          .op = "Const",
          .inputs = {},
          .outputs = {{"sort_strided_slice"}}};
      temp_nodes_.emplace_back(n8);

      const fusion_template::NodeDesc n9 = {
          .key = "sort_strided_slice_stack",
          .op = "Const",
          .inputs = {},
          .outputs = {{"sort_strided_slice"}}};
      temp_nodes_.emplace_back(n9);

      const fusion_template::NodeDesc n10 = {
          .key = "sort_strided_slice_stack_1",
          .op = "Const",
          .inputs = {},
          .outputs = {{"sort_strided_slice"}}};
      temp_nodes_.emplace_back(n10);

      const fusion_template::NodeDesc n11 = {
          .key = "sort_strided_slice_stack_2",
          .op = "Const",
          .inputs = {},
          .outputs = {{"sort_strided_slice"}}};
      temp_nodes_.emplace_back(n11);

      const fusion_template::NodeDesc n12 = {
          .key = "sort_strided_slice",
          .op = "StridedSlice",
          .inputs = {"sort_shape", "sort_strided_slice_stack",
                     "sort_strided_slice_stack_1",
                     "sort_strided_slice_stack_2"},
          .outputs = {{"sort_topkv2"}}};
      temp_nodes_.emplace_back(n12);

      const fusion_template::NodeDesc n13 = {
          .key = "sort_topkv2",
          .op = "TopKV2",
          .inputs = {"sort_neg", "sort_strided_slice"},
          .outputs = {{"sort_neg_1"}}};
      temp_nodes_.emplace_back(n13);

      const fusion_template::NodeDesc n14 = {
          .key = "sort_neg_1",
          .op = "Neg",
          .inputs = {"sort_topkv2"},
          .outputs = {{"sparse_segment_sum_with_num_segments", "1"}}};
      temp_nodes_.emplace_back(n14);

      const fusion_template::NodeDesc n15 = {
          .key = "sparse_segment_sum_with_num_segments",
          .op = "HbSparseSegmentSumWithNumSegments1",
          .inputs = {"1", "argsort_topkv2", "sort_neg_1", "2"},
          .outputs = {{"2"}}};
      temp_nodes_.emplace_back(n15);

      first_key_ = "sparse_segment_sum_with_num_segments";
      num_inputs_ = 3;
      num_outputs_ = 3;
      fused_op_input_idx_.emplace_back(0);
      fused_op_input_idx_.emplace_back(1);
      fused_op_input_idx_.emplace_back(2);
      fused_op_output_idx_.emplace_back(0);
      fused_op_output_idx_.emplace_back(1);
      fused_op_output_idx_.emplace_back(2);
    }
  }

  const string Name() override {
    return "ArgSortAndSparseSegmentReductionFusionTemplate";
  }

  bool AddSubgraph(std::map<std::string, fusion_template::NodeMatching>& nodes,
                   std::string name_postfix, Graph* g,
                   std::vector<const Edge*>& inputs,
                   std::vector<std::vector<const Edge*>>& outputs) override {
    auto origin_device =
        nodes["sparse_segment_sum_with_num_segments"].node->def().device();
    auto input_op_attr = nodes["argsort_neg"].node->def().attr();
    auto segsum_op_attr =
        nodes["sparse_segment_sum_with_num_segments"].node->def().attr();

    NodeDef range_start_def;
    range_start_def.set_op("Const");
    range_start_def.set_name(+"range_start" + name_postfix);
    range_start_def.set_device(origin_device);
    AttrValue attr_type_range_start;
    attr_type_range_start.set_type(DT_INT32);
    range_start_def.mutable_attr()->insert({"dtype", attr_type_range_start});
    Tensor tensor_zero(DT_INT32, {});
    tensor_zero.scalar<int32>()() = 0;
    AttrValue value_zero;
    tensor_zero.AsProtoTensorContent(value_zero.mutable_tensor());
    range_start_def.mutable_attr()->insert({"value", value_zero});

    NodeDef shape_def;
    shape_def.set_op("Shape");
    shape_def.set_name(+"shape" + name_postfix);
    shape_def.set_device(origin_device);
    AttrValue attr_type_range_limit_out;
    attr_type_range_limit_out.set_type(DT_INT32);
    shape_def.mutable_attr()->insert({"T", input_op_attr.at("T")});
    shape_def.mutable_attr()->insert({"out_type", attr_type_range_limit_out});
    AddInput(shape_def, inputs[fused_op_input_idx_[0]]);

    // stridedslice shape
    NodeDef strided_slice_start_def;
    strided_slice_start_def.set_op("Const");
    strided_slice_start_def.set_name(+"strided_slice_start" + name_postfix);
    strided_slice_start_def.set_device(origin_device);
    strided_slice_start_def.mutable_attr()->insert(
        {"dtype", attr_type_range_start});
    Tensor tensor_zero_vec(DT_INT32, {1});
    tensor_zero_vec.flat<int32>()(0) = 0;
    AttrValue value_zero_vec;
    tensor_zero_vec.AsProtoTensorContent(value_zero_vec.mutable_tensor());
    strided_slice_start_def.mutable_attr()->insert({"value", value_zero_vec});

    NodeDef strided_slice_end_def;
    strided_slice_end_def.set_op("Const");
    strided_slice_end_def.set_name(+"strided_slice_end" + name_postfix);
    strided_slice_end_def.set_device(origin_device);
    strided_slice_end_def.mutable_attr()->insert(
        {"dtype", attr_type_range_start});
    Tensor tensor_one_vec(DT_INT32, {1});
    tensor_one_vec.flat<int32>()(0) = 1;
    AttrValue value_one_vec;
    tensor_one_vec.AsProtoTensorContent(value_one_vec.mutable_tensor());
    strided_slice_end_def.mutable_attr()->insert({"value", value_one_vec});

    NodeDef strided_slice_stride_def;
    strided_slice_stride_def.set_op("Const");
    strided_slice_stride_def.set_name(+"strided_slice_stride" + name_postfix);
    strided_slice_stride_def.set_device(origin_device);
    strided_slice_stride_def.mutable_attr()->insert(
        {"dtype", attr_type_range_start});
    strided_slice_stride_def.mutable_attr()->insert({"value", value_one_vec});

    NodeDef strided_slice_def;
    strided_slice_def.set_op("StridedSlice");
    strided_slice_def.set_name(+"strided_slice" + name_postfix);
    strided_slice_def.set_device(origin_device);
    AttrValue attr_type_strided_slice_idx;
    attr_type_strided_slice_idx.set_type(DT_INT32);
    strided_slice_def.mutable_attr()->insert(
        {"Index", attr_type_strided_slice_idx});

    AttrValue attr_type_strided_slice_t;
    attr_type_strided_slice_t.set_type(DT_INT64);
    strided_slice_def.mutable_attr()->insert({"T", attr_type_strided_slice_t});

    AttrValue attr_type_strided_slice_zero;
    SetAttrValue(int(0), &attr_type_strided_slice_zero);
    AttrValue attr_type_strided_slice_one;
    SetAttrValue(int(1), &attr_type_strided_slice_one);
    AttrValue attr_type_strided_slice_two;
    SetAttrValue(int(2), &attr_type_strided_slice_two);

    strided_slice_def.mutable_attr()->insert(
        {"begin_mask", attr_type_strided_slice_zero});
    strided_slice_def.mutable_attr()->insert(
        {"ellipsis_mask", attr_type_strided_slice_zero});
    strided_slice_def.mutable_attr()->insert(
        {"end_mask", attr_type_strided_slice_zero});
    strided_slice_def.mutable_attr()->insert(
        {"new_axis_mask", attr_type_strided_slice_zero});
    strided_slice_def.mutable_attr()->insert(
        {"shrink_axis_mask", attr_type_strided_slice_one});

    strided_slice_def.add_input(absl::StrCat(shape_def.name(), ":", 0));
    strided_slice_def.add_input(
        absl::StrCat(strided_slice_start_def.name(), ":", 0));
    strided_slice_def.add_input(
        absl::StrCat(strided_slice_end_def.name(), ":", 0));
    strided_slice_def.add_input(
        absl::StrCat(strided_slice_stride_def.name(), ":", 0));

    NodeDef range_delta_def;
    range_delta_def.set_op("Const");
    range_delta_def.set_name(+"range_delta" + name_postfix);
    range_delta_def.set_device(origin_device);
    AttrValue attr_type_range_delta;
    attr_type_range_delta.set_type(DT_INT32);
    range_delta_def.mutable_attr()->insert({"dtype", attr_type_range_delta});
    Tensor tensor_one(DT_INT32, {});
    tensor_one.scalar<int32>()() = 1;
    AttrValue value_one;
    tensor_one.AsProtoTensorContent(value_one.mutable_tensor());
    range_delta_def.mutable_attr()->insert({"value", value_one});

    NodeDef range_node_def;
    range_node_def.set_op("Range");
    range_node_def.set_name(+"range" + name_postfix);
    range_node_def.set_device(origin_device);
    range_node_def.mutable_attr()->insert({"Tidx", attr_type_range_limit_out});
    range_node_def.add_input(absl::StrCat(range_start_def.name(), ":", 0));
    range_node_def.add_input(absl::StrCat(strided_slice_def.name(), ":", 0));
    range_node_def.add_input(absl::StrCat(range_delta_def.name(), ":", 0));

    NodeDef segsum_node_def;
    segsum_node_def.set_op("SparseSegmentSumWithNumSegments");
    segsum_node_def.set_name(+"sparse_segment_sum_with_num_segments" +
                             name_postfix);
    segsum_node_def.set_device(origin_device);
    segsum_node_def.mutable_attr()->insert({"T", segsum_op_attr.at("T")});
    segsum_node_def.mutable_attr()->insert({"Tidx", segsum_op_attr.at("Tidx")});
    segsum_node_def.mutable_attr()->insert(
        {"Tnumsegments", segsum_op_attr.at("Tnumsegments")});

    AddInput(segsum_node_def, inputs[fused_op_input_idx_[1]]);
    segsum_node_def.add_input(absl::StrCat(range_node_def.name(), ":", 0));
    AddInput(segsum_node_def, inputs[fused_op_input_idx_[0]]);
    AddInput(segsum_node_def, inputs[fused_op_input_idx_[2]]);

    // rebuild the graph
    Status status;
    Node* range_start_node = g->AddNode(range_start_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* shape_node = g->AddNode(shape_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* strided_slice_start_node =
        g->AddNode(strided_slice_start_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* strided_slice_end_node = g->AddNode(strided_slice_end_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* strided_slice_stride_node =
        g->AddNode(strided_slice_stride_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* strided_slice_node = g->AddNode(strided_slice_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* range_delta_node = g->AddNode(range_delta_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* range_node_node = g->AddNode(range_node_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }
    Node* segsum_node_node = g->AddNode(segsum_node_def, &status);
    if (status != Status::OK()) {
      VLOG(1) << status.error_message();
      return false;
    }

    Node* segids_node = inputs[fused_op_input_idx_[0]]->src();
    int segids_node_out_port = inputs[fused_op_input_idx_[0]]->src_output();
    Node* params_node = inputs[fused_op_input_idx_[1]]->src();
    int params_node_out_port = inputs[fused_op_input_idx_[1]]->src_output();
    Node* numsegs_node = inputs[fused_op_input_idx_[2]]->src();
    int numsegs_node_out_port = inputs[fused_op_input_idx_[2]]->src_output();

    g->AddEdge(segids_node, segids_node_out_port, shape_node, 0);
    g->AddEdge(shape_node, 0, strided_slice_node, 0);
    g->AddEdge(strided_slice_start_node, 0, strided_slice_node, 1);
    g->AddEdge(strided_slice_end_node, 0, strided_slice_node, 2);
    g->AddEdge(strided_slice_stride_node, 0, strided_slice_node, 3);

    g->AddEdge(range_start_node, 0, range_node_node, 0);
    g->AddEdge(strided_slice_node, 0, range_node_node, 1);
    g->AddEdge(range_delta_node, 0, range_node_node, 2);

    g->AddEdge(params_node, params_node_out_port, segsum_node_node, 0);
    g->AddEdge(range_node_node, 0, segsum_node_node, 1);
    g->AddEdge(segids_node, segids_node_out_port, segsum_node_node, 2);
    g->AddEdge(numsegs_node, numsegs_node_out_port, segsum_node_node, 3);

    for (auto* ori_edge : outputs[fused_op_output_idx_[0]]) {
      if (ori_edge != nullptr && ori_edge->dst() != nullptr) {
        g->AddEdge(range_node_node, 0, ori_edge->dst(), ori_edge->dst_input());
      }
    }
    for (auto* ori_edge : outputs[fused_op_output_idx_[1]]) {
      if (ori_edge != nullptr && ori_edge->dst() != nullptr) {
        g->AddEdge(segids_node, 0, ori_edge->dst(), ori_edge->dst_input());
      }
    }
    for (auto* ori_edge : outputs[fused_op_output_idx_[2]]) {
      if (ori_edge != nullptr && ori_edge->dst() != nullptr) {
        g->AddEdge(segsum_node_node, 0, ori_edge->dst(), ori_edge->dst_input());
      }
    }

    // remove stale nodes
    for (auto matched_node_itr : nodes) {
      Node* stale_node = const_cast<Node*>(matched_node_itr.second.node);
      g->RemoveNode(stale_node);
    }
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

inline bool SparseSegmentReductionOptimizationDisabled() {
  static const bool kSparseSegmentReductionOptimizationDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_SEGMENT_REDUCTION_OPTIMIZATION_DISABLED", false);
  return kSparseSegmentReductionOptimizationDisabled;
}

inline bool SegmentReductionRelocationDisabled() {
  static const bool kSegmentReductionRelocationDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_SEGMENT_REDUCTION_RELOCATION_DISABLED", false);
  return kSegmentReductionRelocationDisabled;
}

inline bool SegmentReductionArgSortFusionDisabled() {
  static const bool kSegmentReductionArgSortFusionDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_SEGMENT_REDUCTION_ARGSORT_FUSION_DISABLED", false);
  return kSegmentReductionArgSortFusionDisabled;
}

inline bool SegmentReductionPackingDisabled() {
  static const bool kSegmentReductionPackingDisabled =
      ::hybridbackend::EnvVarGetBool(
          "HB_OP_SPARSE_SEGMENT_REDUCTION_PACKING_DISABLED", false);
  return kSegmentReductionPackingDisabled;
}

}  // namespace

class OptimizeSparseSegmentReductionReplacingPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_FALSE(disabled ||
                         SparseSegmentReductionOptimizationDisabled())) {
      return Status::OK();
    }

    if (TF_PREDICT_TRUE(!SegmentReductionRelocationDisabled())) {
      Relocate("SparseSegmentSum").WithInput(0).In(graph);
      Relocate("SparseSegmentSumWithNumSegments").WithInput(0).In(graph);
      Relocate("UnsortedSegmentSum").WithInput(0).In(graph);
    }

    TF_RETURN_IF_ERROR(Replace("SparseSegmentSum", "HbSparseSegmentSum1")
                           .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_FLOAT,
                                               DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));
    TF_RETURN_IF_ERROR(Replace("SparseSegmentMean", "HbSparseSegmentMean1")
                           .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));
    TF_RETURN_IF_ERROR(Replace("SparseSegmentSqrtN", "HbSparseSegmentSqrtN1")
                           .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));

    TF_RETURN_IF_ERROR(Replace("SparseSegmentSumWithNumSegments",
                               "HbSparseSegmentSumWithNumSegments1")
                           .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_FLOAT,
                                               DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                           .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));
    TF_RETURN_IF_ERROR(Replace("SparseSegmentMeanWithNumSegments",
                               "HbSparseSegmentMeanWithNumSegments1")
                           .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                           .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));
    TF_RETURN_IF_ERROR(Replace("SparseSegmentSqrtNWithNumSegments",
                               "HbSparseSegmentSqrtNWithNumSegments1")
                           .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                           .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));

    TF_RETURN_IF_ERROR(
        Replace("SparseSegmentMeanGrad", "HbSparseSegmentMeanGrad1")
            .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
            .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
            .Packed()
            .In(graph));
    TF_RETURN_IF_ERROR(
        Replace("SparseSegmentSqrtNGrad", "HbSparseSegmentSqrtNGrad1")
            .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
            .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
            .Packed()
            .In(graph));
    TF_RETURN_IF_ERROR(Replace("UnsortedSegmentSum", "HbUnsortedSegmentSum1")
                           .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_FLOAT,
                                               DT_DOUBLE, DT_HALF})
                           .WithTypeAttr("Tindices", {DT_INT64, DT_INT32})
                           .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                           .Packed()
                           .In(graph));

    return Status::OK();
  }
};  // namespace hybridbackend

REGISTER_REPLACING_OPTIMIZATION(OptimizeSparseSegmentReductionReplacingPass);

class OptimizeSparseSegmentReductionReductionPass : public OpOptimizationPass {
 public:
  Status Optimize(Graph* graph, const SessionOptions* options,
                  const bool disabled) override {
    if (TF_PREDICT_FALSE(disabled ||
                         SparseSegmentReductionOptimizationDisabled())) {
      return Status::OK();
    }

    if (TF_PREDICT_TRUE(!SegmentReductionArgSortFusionDisabled())) {
      ArgSortAndSparseSegmentReductionFusionTemplate fusion_template;
      Fuse(graph, fusion_template);
    }

    if (TF_PREDICT_TRUE(!SegmentReductionPackingDisabled())) {
      TF_RETURN_IF_ERROR(Pack("HbSparseSegmentSum1", "HbSparseSegmentSumN")
                             .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_FLOAT,
                                                 DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                             .In(graph));
      TF_RETURN_IF_ERROR(Pack("HbSparseSegmentMean1", "HbSparseSegmentMeanN")
                             .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                             .In(graph));
      TF_RETURN_IF_ERROR(Pack("HbSparseSegmentSqrtN1", "HbSparseSegmentSqrtNN")
                             .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                             .In(graph));

      TF_RETURN_IF_ERROR(Pack("HbSparseSegmentSumWithNumSegments1",
                              "HbSparseSegmentSumWithNumSegmentsN")
                             .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_FLOAT,
                                                 DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                             .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                             .In(graph));
      TF_RETURN_IF_ERROR(Pack("HbSparseSegmentMeanWithNumSegments1",
                              "HbSparseSegmentMeanWithNumSegmentsN")
                             .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                             .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                             .In(graph));
      TF_RETURN_IF_ERROR(Pack("HbSparseSegmentSqrtNWithNumSegments1",
                              "HbSparseSegmentSqrtNWithNumSegmentsN")
                             .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
                             .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                             .In(graph));

      TF_RETURN_IF_ERROR(
          Pack("HbSparseSegmentMeanGrad1", "HbSparseSegmentMeanGradN")
              .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
              .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
              .In(graph));
      TF_RETURN_IF_ERROR(
          Pack("HbSparseSegmentSqrtNGrad1", "HbSparseSegmentSqrtNGradN")
              .WithTypeAttr("T", {DT_FLOAT, DT_DOUBLE, DT_HALF})
              .WithTypeAttr("Tidx", {DT_INT64, DT_INT32})
              .In(graph));
      TF_RETURN_IF_ERROR(Pack("HbUnsortedSegmentSum1", "HbUnsortedSegmentSumN")
                             .WithTypeAttr("T", {DT_INT64, DT_INT32, DT_FLOAT,
                                                 DT_DOUBLE, DT_HALF})
                             .WithTypeAttr("Tindices", {DT_INT64, DT_INT32})
                             .WithTypeAttr("Tnumsegments", {DT_INT64, DT_INT32})
                             .In(graph));

      return Status::OK();
    }

    return Status::OK();
  }
};

REGISTER_REDUCTION_OPTIMIZATION(OptimizeSparseSegmentReductionReductionPass);

}  // namespace hybridbackend
}  // namespace tensorflow

#endif  // HYBRIDBACKEND_TENSORFLOW
