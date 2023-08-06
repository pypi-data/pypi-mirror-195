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

r'''SparseFillEmptyRows Op Test.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest

import numpy as np
import tensorflow as tf

import hybridbackend.common.test as hbtest
import hybridbackend.tensorflow as hb  # pylint: disable=unused-import


# pylint: disable=missing-docstring
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_CUDA') == 'ON', 'GPU required')
class SparseFillEmptyRowsTest(unittest.TestCase):
  def setUp(self):  # pylint: disable=invalid-name
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    hb.enable_optimization(logging_level=2)
    hb.sparse.fill_empty_rows.enable_optimization(logging_level=2)

  def tearDown(self):  # pylint: disable=invalid-name
    del os.environ['CUDA_VISIBLE_DEVICES']

  def _input_value_5x6(self, dtype=np.int32):
    ind = np.array([[0, 0], [1, 0], [1, 3], [1, 4], [3, 2], [3, 3]])
    val = np.array([0, 10, 13, 14, 32, 33])
    shape = np.array([5, 6])
    return tf.SparseTensorValue(
      np.array(ind, np.int64),
      np.array(val, dtype),
      np.array(shape, np.int64))

  def _input_5x6(self):
    return tf.SparseTensor.from_value(self._input_value_5x6())

  def test_input_5x6(self):
    with tf.Graph().as_default() as g:
      with tf.device('/gpu:0'):
        out, ind = tf.sparse.fill_empty_rows(self._input_5x6(), -1)
        with tf.Session(graph=g) as sess:
          tf_out, tf_ind = sess.run([out, ind])
          np.testing.assert_equal(
            tf_out.indices,
            [[0, 0], [1, 0], [1, 3], [1, 4], [3, 2], [3, 3], [2, 0], [4, 0]])
          np.testing.assert_equal(
            tf_out.values,
            [0, 10, 13, 14, 32, 33, -1, -1])
          np.testing.assert_equal(
            tf_out.dense_shape,
            [5, 6])
          np.testing.assert_equal(
            tf_ind,
            np.array([0, 0, 1, 0, 1]).astype(bool))

  def _input_2x6(self):
    ind = np.array([[0, 0], [1, 0], [1, 3], [1, 4]])
    val = np.array([0, 10, 13, 14])
    shape = np.array([2, 6])
    return tf.SparseTensor(
      tf.constant(ind, tf.int64),
      tf.constant(val, tf.int32),
      tf.constant(shape, tf.int64))

  def test_input_2x6(self):
    with tf.Graph().as_default() as g:
      with tf.device('/gpu:0'):
        out, ind = tf.sparse.fill_empty_rows(self._input_2x6(), -1)
        with tf.Session(graph=g) as sess:
          tf_out, tf_ind = sess.run([out, ind])
        np.testing.assert_equal(
          tf_out.indices,
          [[0, 0], [1, 0], [1, 3], [1, 4]])
        np.testing.assert_equal(tf_out.values, [0, 10, 13, 14])
        np.testing.assert_equal(tf_out.dense_shape, [2, 6])
        np.testing.assert_equal(tf_ind, np.zeros(2).astype(bool))

  def test_2_inputs(self):
    with tf.Graph().as_default() as g:
      with tf.device('/gpu:0'):
        out1, ind1 = tf.sparse.fill_empty_rows(self._input_5x6(), -1)
        out2, ind2 = tf.sparse.fill_empty_rows(self._input_5x6(), -1)
        with tf.Session(graph=g) as sess:
          tf_out1, tf_ind1, tf_out2, tf_ind2 = sess.run(
            [out1, ind1, out2, ind2])
          np.testing.assert_equal(
            tf_out1.indices,
            [[0, 0], [1, 0], [1, 3], [1, 4], [3, 2], [3, 3], [2, 0], [4, 0]])
          np.testing.assert_equal(
            tf_out1.values,
            [0, 10, 13, 14, 32, 33, -1, -1])
          np.testing.assert_equal(
            tf_out1.dense_shape,
            [5, 6])
          np.testing.assert_equal(
            tf_ind1,
            np.array([0, 0, 1, 0, 1]).astype(bool))
          np.testing.assert_equal(
            tf_out2.indices,
            [[0, 0], [1, 0], [1, 3], [1, 4], [3, 2], [3, 3], [2, 0], [4, 0]])
          np.testing.assert_equal(
            tf_out2.values,
            [0, 10, 13, 14, 32, 33, -1, -1])
          np.testing.assert_equal(
            tf_out2.dense_shape,
            [5, 6])
          np.testing.assert_equal(
            tf_ind2,
            np.array([0, 0, 1, 0, 1]).astype(bool))


if __name__ == '__main__':
  hbtest.main()
