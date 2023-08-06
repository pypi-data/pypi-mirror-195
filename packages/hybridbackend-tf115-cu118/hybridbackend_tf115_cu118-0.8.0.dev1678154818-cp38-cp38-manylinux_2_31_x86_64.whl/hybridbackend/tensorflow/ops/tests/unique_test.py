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

r'''Unique Op Test.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest

import numpy as np
import tensorflow as tf

import hybridbackend.common.test as hbtest
import hybridbackend.tensorflow as hb


# pylint: disable=missing-docstring
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_CUDA') == 'ON', 'GPU required')
class UniqueTest(unittest.TestCase):
  def setUp(self):  # pylint: disable=invalid-name
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    hb.enable_optimization(logging_level=2)
    hb.unique.enable_optimization(logging_level=2)

  def tearDown(self):  # pylint: disable=invalid-name
    del os.environ['CUDA_VISIBLE_DEVICES']

  def test_int64_input(self):
    np.random.seed(0)
    x = np.random.randint(
      low=-1000000000,
      high=1000000000,
      size=10000,
      dtype=np.int64)

    with tf.Graph().as_default(), hb.scope():
      with tf.device('/gpu:0'):
        y, idx = tf.unique(x)
      with tf.train.MonitoredTrainingSession('') as sess:
        tf_y, tf_idx = sess.run([y, idx])

    np.testing.assert_equal(len(x), len(tf_idx))
    np.testing.assert_equal(len(tf_y), len(np.unique(x)))
    for expect, idx in zip(x, tf_idx):
      np.testing.assert_equal(expect, tf_y[idx])

  def test_int32_input(self):
    np.random.seed(0)
    x = np.random.randint(
      low=-1000000000,
      high=1000000000,
      size=100000,
      dtype=np.int32)

    with tf.Graph().as_default(), hb.scope():
      with tf.device('/gpu:0'):
        y, idx = tf.unique(x)
      with tf.train.MonitoredTrainingSession('') as sess:
        tf_y, tf_idx = sess.run([y, idx])

    np.testing.assert_equal(len(x), len(tf_idx))
    np.testing.assert_equal(len(tf_y), len(np.unique(x)))
    for expect, idx in zip(x, tf_idx):
      np.testing.assert_equal(expect, tf_y[idx])

  def test_empty_input(self):
    x = np.array([], np.int64)

    with tf.Graph().as_default(), hb.scope():
      with tf.device('/gpu:0'):
        y, idx = tf.unique(x)
      with tf.train.MonitoredTrainingSession('') as sess:
        tf_y, tf_idx = sess.run([y, idx])

    np.testing.assert_equal(0, len(tf_y))
    np.testing.assert_equal(0, len(tf_idx))

  def test_2out_input(self):
    np.random.seed(0)
    x = np.random.randint(
      low=-1000000000,
      high=1000000000,
      size=100000,
      dtype=np.int32)
    secs = [30000]
    _, x2 = np.split(x, secs)

    with tf.Graph().as_default(), hb.scope():
      with tf.device('/gpu:0'):
        _, xx = tf.split(x, [30000, 70000])
        y2, idx2 = tf.unique(xx)
      with tf.train.MonitoredTrainingSession('') as sess:
        tf_y2, tf_idx2 = sess.run([y2, idx2])

    np.testing.assert_equal(len(x2), len(tf_idx2))
    np.testing.assert_equal(len(tf_y2), len(np.unique(x2)))
    for expect, idx in zip(x2, tf_idx2):
      np.testing.assert_equal(expect, tf_y2[idx])

  def test_multi_ways(self):
    np.random.seed(0)
    num_inputs = 4
    inputs = []
    for _ in range(num_inputs):
      inputs.append(
        np.random.randint(
          low=-1000000000,
          high=1000000000,
          size=10000,
          dtype=np.int64))

    with tf.Graph().as_default(), hb.scope():
      with tf.device('/gpu:0'):
        outputs = []
        output_indices = []
        for i in range(num_inputs):
          y, idx = tf.unique(inputs[i])
          outputs.append(y)
          output_indices.append(idx)

      with tf.train.MonitoredTrainingSession('') as sess:
        results = sess.run(
          {'outputs': outputs, 'output_indices': output_indices})

    for i in range(num_inputs):
      np.testing.assert_equal(len(inputs[i]), len(results['output_indices'][i]))
      np.testing.assert_equal(
        len(results['outputs'][i]), len(np.unique(inputs[i])))
      for expect, idx in zip(inputs[i], results['output_indices'][i]):
        np.testing.assert_equal(expect, results['outputs'][i][idx])


if __name__ == '__main__':
  hbtest.main()
