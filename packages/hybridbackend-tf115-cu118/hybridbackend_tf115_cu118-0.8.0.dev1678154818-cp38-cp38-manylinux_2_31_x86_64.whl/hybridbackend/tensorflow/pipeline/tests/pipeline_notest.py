# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

r'''Tests for pipelined layers.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest

import numpy as np

import hybridbackend.common.test as hbtest


def _test_pipeline_ga(_, lr, pipeline_num=-1):
  '''Testing composed layers within pipeline.
  '''
  # pylint: disable=import-outside-toplevel
  import tensorflow as tf

  import hybridbackend.tensorflow as hb

  @hb.function(seed=42,
               emb_num_groups=None,
               emb_unique={'ad0': False},
               pipeline_num=pipeline_num,
               pipeline_dense_ga_only=True)
  def train_fn():
    columns = [
      tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_identity(
          key='ad0', num_buckets=10, default_value=0),
        dimension=20,
        initializer=tf.constant_initializer(0.5)),
      tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_identity(
          key='ad1', num_buckets=10, default_value=0),
        dimension=30,
        initializer=tf.constant_initializer(0.5)),
      tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_identity(
          key='ad2', num_buckets=10, default_value=0),
        dimension=40,
        initializer=tf.constant_initializer(0.5)),
      tf.feature_column.embedding_column(
        tf.feature_column.categorical_column_with_identity(
          key='user0', num_buckets=10, default_value=0),
        dimension=20,
        initializer=tf.constant_initializer(0.5))
    ]
    features = {
      'ad0': tf.constant([0, 1, 3, 2, 0, 1, 3, 2]),
      'ad1': tf.constant([1, 5, 3, 4, 1, 5, 3, 4]),
      'ad2': tf.constant([5, 2, 7, 4, 5, 2, 7, 4]),
      'user0': tf.constant([2, 5, 4, 7, 2, 5, 4, 7])
    }
    emb_output = tf.keras.layers.DenseFeatures(columns)(features)
    seq = tf.keras.Sequential()
    seq.add(
      tf.keras.layers.Dense(
        10, name='aaa_dense',
        input_dim=110,
        activation=tf.math.sigmoid))
    seq.add(tf.keras.layers.Lambda(tf.reduce_mean))
    if pipeline_num > 1:
      pipelined_layers = hb.pipeline.Pipeline(name='add_pipe')
      pipelined_layers.add(seq, training=True)
      loss = pipelined_layers(emb_output)
    else:
      loss = seq.call(emb_output)
    opt = tf.train.AdamOptimizer(lr)
    step = tf.train.get_or_create_global_step()
    train_op = opt.minimize(loss, global_step=step)
    return loss, train_op

  with hb.pipeline.scope():
    loss, train_op = train_fn()

  steps = []
  with tf.train.MonitoredTrainingSession(
    '',
    hooks=[
      tf.train.StopAtStepHook(last_step=100),
      tf.train.NanTensorHook(loss),
      tf.train.LoggingTensorHook(
        tensors={'loss': loss},
        every_n_iter=20)]) as sess:
    while not sess.should_stop():
      steps.append(sess.run(loss))
      steps.append(sess.run(train_op))
  return steps


# pylint: disable=missing-docstring
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_CUDA') == 'ON', 'GPU required')
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_NCCL') == 'ON', 'NCCL required')
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_TENSORFLOW_ESTIMATOR') != 'OFF',
  'TF Estimator required')
class PipelineTest(unittest.TestCase):
  '''Tests for Gradient Aggregation in Pipeline.
  '''
  def setUp(self):  # pylint: disable=invalid-name
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

  def tearDown(self):  # pylint: disable=invalid-name
    del os.environ['CUDA_VISIBLE_DEVICES']

  def test_pipeline_ga(self):
    results_v1 = hbtest.Spawn()(
      lambda rank: _test_pipeline_ga(rank, 0.0001))
    results_v2 = hbtest.Spawn()(
      lambda rank: _test_pipeline_ga(rank, 0.0001, pipeline_num=2))
    np.testing.assert_allclose(results_v1[0][0], results_v2[0][0], rtol=1e-6)


if __name__ == '__main__':
  hbtest.main(f'{__file__}.xml')
