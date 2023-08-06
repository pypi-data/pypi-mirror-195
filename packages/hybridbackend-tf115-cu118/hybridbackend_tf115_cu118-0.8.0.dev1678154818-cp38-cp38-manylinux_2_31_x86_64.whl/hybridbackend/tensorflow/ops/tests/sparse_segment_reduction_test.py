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

r'''Group SegmentReduction Ops Test.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import unittest

import numpy as np
import tensorflow as tf

import hybridbackend.common.test as hbtest
import hybridbackend.tensorflow as hb  # pylint: disable=unused-import


# pylint: disable=missing-docstring
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_CUDA') == 'ON', 'GPU required')
class SparseSegmentReductionOpsTest(unittest.TestCase):
  def setUp(self):  # pylint: disable=invalid-name
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    hb.enable_optimization(logging_level=2)
    hb.sparse.segment.enable_optimization(logging_level=2)

  def tearDown(self):  # pylint: disable=invalid-name
    del os.environ['CUDA_VISIBLE_DEVICES']

  def _create_test_data(self, num_columns, answer_val):
    np.random.seed(0)
    data = [
      np.full((100, 10), 1.0, dtype=float)
      for i in range(num_columns)]
    indices = [
      np.arange(100, dtype=np.int32)
      for i in range(num_columns)]
    seg_ids = [
      np.concatenate(
        (np.arange(50, dtype=np.int32), np.arange(50, dtype=np.int32)), axis=0)
      for i in range(num_columns)]
    answer = [
      np.full((50, 10), answer_val, dtype=float)
      for i in range(num_columns)]
    return data, indices, seg_ids, answer

  def test_sparse_segment_sum(self):
    num_columns = 10
    data, indices, seg_ids, answer = self._create_test_data(num_columns, 2.0)
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        indices_in = [tf.constant(d) for d in indices]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        out = [
          tf.sparse.segment_sum(data_in[i], indices_in[i], seg_ids_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def test_unsorted_segment_sum(self):
    num_columns = 10
    data, _, seg_ids, answer = self._create_test_data(num_columns, 2.0)
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        num_segments_in = [
          tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
        out = [
          tf.math.unsorted_segment_sum(
            data_in[i], seg_ids_in[i], num_segments_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def test_sparse_segment_sum_with_num_segments(self):
    num_columns = 10
    data, indices, seg_ids, answer = self._create_test_data(num_columns, 2.0)
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        indices_in = [tf.constant(d) for d in indices]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        num_segments_in = [
          tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
        out = [
          tf.sparse.segment_sum(
            data_in[i], indices_in[i], seg_ids_in[i],
            num_segments=num_segments_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def test_sparse_segment_mean(self):
    num_columns = 10
    data, indices, seg_ids, answer = self._create_test_data(num_columns, 1.0)
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        indices_in = [tf.constant(d) for d in indices]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        out = [
          tf.sparse.segment_mean(data_in[i], indices_in[i], seg_ids_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def test_sparse_segment_mean_with_num_segments(self):
    num_columns = 10
    data, indices, seg_ids, answer = self._create_test_data(num_columns, 1.0)
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        indices_in = [tf.constant(d) for d in indices]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        num_segments_in = [
          tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
        out = [
          tf.sparse.segment_mean(
            data_in[i], indices_in[i], seg_ids_in[i],
            num_segments=num_segments_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def test_sparse_segment_sqrtn(self):
    num_columns = 10
    data, indices, seg_ids, answer = self._create_test_data(
      num_columns, 2.0 / math.sqrt(2.0))
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        indices_in = [tf.constant(d) for d in indices]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        out = [
          tf.sparse.segment_sqrt_n(data_in[i], indices_in[i], seg_ids_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def test_sparse_segment_sqrtn_with_num_segments(self):
    num_columns = 10
    data, indices, seg_ids, answer = self._create_test_data(
      num_columns, 2.0 / math.sqrt(2.0))
    with tf.Graph().as_default():
      with tf.device('/gpu:0'):
        data_in = [tf.constant(d) for d in data]
        indices_in = [tf.constant(d) for d in indices]
        seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
        num_segments_in = [
          tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
        out = [
          tf.sparse.segment_sqrt_n(
            data_in[i], indices_in[i], seg_ids_in[i],
            num_segments=num_segments_in[i])
          for i in range(num_columns)]
        with tf.Session() as sess:
          out_value = sess.run(out)
    for c in range(num_columns):
      np.testing.assert_equal(out_value[c], answer[c])

  def _create_test_data_grad(self, num_columns):
    np.random.seed(0)
    data = [
      np.full((100, 10), 1.0, dtype=float)
      for i in range(num_columns)]
    indices = [
      np.arange(100, dtype=np.int32)
      for i in range(num_columns)]
    seg_ids = [
      np.concatenate(
        (np.arange(50, dtype=np.int32), np.arange(50, dtype=np.int32)), axis=0)
      for i in range(num_columns)]
    return data, indices, seg_ids

  def test_sparse_segment_sum_grad(self):
    num_columns = 2
    data, indices, seg_ids = self._create_test_data_grad(num_columns)
    with tf.Graph().as_default():
      with tf.Session():
        with tf.device('/gpu:0'):
          data_in = [tf.constant(d) for d in data]
          indices_in = [tf.constant(d) for d in indices]
          seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
          out = [
            tf.sparse.segment_sum(data_in[i], indices_in[i], seg_ids_in[i])
            for i in range(num_columns)]
          for c in range(num_columns):
            jacob_t, jacob_n = tf.test.compute_gradient(
              data_in[c],
              [100, 10],
              out[c], [50, 10],
              x_init_value=data[c],
              delta=1)
            np.testing.assert_allclose(jacob_t, jacob_n)

  def test_sparse_segment_sum_with_num_segments_grad(self):
    num_columns = 2
    data, indices, seg_ids = self._create_test_data_grad(num_columns)
    with tf.Graph().as_default():
      with tf.Session():
        with tf.device('/gpu:0'):
          data_in = [tf.constant(d) for d in data]
          indices_in = [tf.constant(d) for d in indices]
          seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
          num_segments_in = [
            tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
          out = [
            tf.sparse.segment_sum(
              data_in[i], indices_in[i], seg_ids_in[i],
              num_segments=num_segments_in[i])
            for i in range(num_columns)]
          for c in range(num_columns):
            jacob_t, jacob_n = tf.test.compute_gradient(
              data_in[c],
              [100, 10],
              out[c], [50, 10],
              x_init_value=data[c],
              delta=1)
            np.testing.assert_allclose(jacob_t, jacob_n)

  def test_sparse_segment_mean_grad(self):
    num_columns = 2
    data, indices, seg_ids = self._create_test_data_grad(num_columns)
    with tf.Graph().as_default():
      with tf.Session():
        with tf.device('/gpu:0'):
          data_in = [tf.constant(d) for d in data]
          indices_in = [tf.constant(d) for d in indices]
          seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
          out = [
            tf.sparse.segment_mean(data_in[i], indices_in[i], seg_ids_in[i])
            for i in range(num_columns)]
          for c in range(num_columns):
            jacob_t, jacob_n = tf.test.compute_gradient(
              data_in[c],
              [100, 10],
              out[c], [50, 10],
              x_init_value=data[c],
              delta=1)
            np.testing.assert_allclose(jacob_t, jacob_n)

  def test_sparse_segment_mean_with_num_segments_grad(self):
    num_columns = 2
    data, indices, seg_ids = self._create_test_data_grad(num_columns)
    with tf.Graph().as_default():
      with tf.Session():
        with tf.device('/gpu:0'):
          data_in = [tf.constant(d) for d in data]
          indices_in = [tf.constant(d) for d in indices]
          seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
          num_segments_in = [
            tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
          out = [
            tf.sparse.segment_mean(
              data_in[i], indices_in[i], seg_ids_in[i],
              num_segments=num_segments_in[i])
            for i in range(num_columns)]
          for c in range(num_columns):
            jacob_t, jacob_n = tf.test.compute_gradient(
              data_in[c],
              [100, 10],
              out[c], [50, 10],
              x_init_value=data[c],
              delta=1)
            np.testing.assert_allclose(jacob_t, jacob_n)

  def test_sparse_segment_sqrtn_grad(self):
    num_columns = 2
    data, indices, seg_ids = self._create_test_data_grad(num_columns)
    with tf.Graph().as_default():
      with tf.Session():
        with tf.device('/gpu:0'):
          data_in = [tf.constant(d) for d in data]
          indices_in = [tf.constant(d) for d in indices]
          seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
          out = [
            tf.sparse.segment_sqrt_n(data_in[i], indices_in[i], seg_ids_in[i])
            for i in range(num_columns)]
          for c in range(num_columns):
            jacob_t, jacob_n = tf.test.compute_gradient(
              data_in[c],
              [100, 10],
              out[c], [50, 10],
              x_init_value=data[c],
              delta=1)
            np.testing.assert_allclose(jacob_t, jacob_n)

  def test_sparse_segment_sqrtn_with_num_segments_grad(self):
    num_columns = 2
    data, indices, seg_ids = self._create_test_data_grad(num_columns)
    with tf.Graph().as_default():
      with tf.Session():
        with tf.device('/gpu:0'):
          data_in = [tf.constant(d) for d in data]
          indices_in = [tf.constant(d) for d in indices]
          seg_ids_in = [tf.sort(tf.constant(d)) for d in seg_ids]
          num_segments_in = [
            tf.constant(50, dtype=tf.int32) for _ in range(num_columns)]
          out = [
            tf.sparse.segment_sqrt_n(
              data_in[i], indices_in[i], seg_ids_in[i],
              num_segments=num_segments_in[i])
            for i in range(num_columns)]
          for c in range(num_columns):
            jacob_t, jacob_n = tf.test.compute_gradient(
              data_in[c],
              [100, 10],
              out[c], [50, 10],
              x_init_value=data[c],
              delta=1)
            np.testing.assert_allclose(jacob_t, jacob_n)


if __name__ == '__main__':
  hbtest.main()
