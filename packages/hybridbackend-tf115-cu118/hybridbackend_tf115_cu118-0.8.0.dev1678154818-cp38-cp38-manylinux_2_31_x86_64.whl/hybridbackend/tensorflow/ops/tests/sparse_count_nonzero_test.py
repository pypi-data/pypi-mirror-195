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

r'''Sparse Count Nonzero Ops Test.
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
from hybridbackend.tensorflow.ops.sparse.count_nonzero.ops import \
  sparse_count_nonzero as count_nonzero


# pylint: disable=missing-docstring
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_CUDA') == 'ON', 'GPU required')
class SparseCountNonzeroOpsTest(unittest.TestCase):
  def setUp(self):  # pylint: disable=invalid-name
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    hb.enable_optimization(logging_level=2)
    hb.sparse.count_nonzero.enable_optimization(logging_level=2)

  def tearDown(self):  # pylint: disable=invalid-name
    del os.environ['CUDA_VISIBLE_DEVICES']

  def test_sparse_count_nonzero(self):
    with tf.Graph().as_default(), hb.scope():
      tensor_to_count = tf.sparse.SparseTensor(
        indices=[[0, 1, 1], [0, 2, 1], [1, 0, 1], [1, 2, 1]],
        values=tf.constant([0, 1, 2, 2]),
        dense_shape=[2, 3, 2])
      out_a = count_nonzero(
        tensor_to_count, axis=-1, dtype=tf.int64)
      out_b = tf.math.count_nonzero(
        tf.sparse.to_dense(tensor_to_count),
        axis=-1, dtype=tf.int64)
      with tf.train.MonitoredTrainingSession('') as sess:
        out_value_a, out_value_b = sess.run([out_a, out_b])
      np.testing.assert_equal(out_value_a, out_value_b)


if __name__ == '__main__':
  hbtest.main()
