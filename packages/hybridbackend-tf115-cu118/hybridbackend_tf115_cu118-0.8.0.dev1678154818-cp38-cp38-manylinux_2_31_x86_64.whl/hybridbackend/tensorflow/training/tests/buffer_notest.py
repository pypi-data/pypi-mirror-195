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

r'''Tests for embedding buffers.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import unittest

import numpy as np
import tensorflow as tf
from tensorflow.python.feature_column import feature_column_v2 as fc

import hybridbackend.common.test as hbtest
import hybridbackend.tensorflow as hb


# pylint: disable=missing-docstring
# pylint: disable=import-outside-toplevel
@unittest.skipUnless(
  os.getenv('HYBRIDBACKEND_WITH_CUDA') == 'ON', 'GPU required')
class EmbeddingBufferTest(unittest.TestCase):
  '''Tests for embedding columns.
  '''
  def setUp(self):  # pylint: disable=invalid-name
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

  def tearDown(self):  # pylint: disable=invalid-name
    del os.environ['CUDA_VISIBLE_DEVICES']

  def _test_1_col_1_step(self, seed):
    with tf.Graph().as_default():
      with hb.scope(
          seed=seed,
          comm_pool_name='test_1_col_1_step',
          emb_buffer_size=10,
          emb_device='/cpu:0'):
        columns = [
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='ad0', num_buckets=20, default_value=0),
            dimension=20,
            initializer=tf.constant_initializer(0.5)),
        ]
        features = {
          'ad0': tf.constant([0, 1, 3, 2])
        }
        out_emb = tf.keras.layers.DenseFeatures(columns)(features)
        loss = tf.reduce_mean(out_emb)
        step = tf.train.get_or_create_global_step()

        final_loss = None
        with tf.train.MonitoredTrainingSession(
            '',
            hooks=[
              tf.train.StopAtStepHook(last_step=100),
              tf.train.NanTensorHook(loss),
              tf.train.LoggingTensorHook(
                tensors={'loss': loss, 'step': step},
                every_n_iter=20)]) as sess:
          final_loss = sess.run(loss)
        return final_loss

  def test_1_col_1_step(self):
    final_loss = self._test_1_col_1_step(42)
    np.testing.assert_allclose(final_loss, 0.5, rtol=1e-6)

  def _test_1_col_2_steps(self, seed, lr):
    with tf.Graph().as_default():
      with hb.scope(
          seed=seed,
          comm_pool_name='test_1_col_2_steps',
          emb_buffer_size=10,
          emb_device='/cpu:0'):
        columns = [
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='ad0', num_buckets=20, default_value=0),
            dimension=20,
            initializer=tf.constant_initializer(0.5)),
        ]
        features = {
          'ad0': tf.constant([0, 1, 3, 2])
        }
        out_emb = tf.keras.layers.DenseFeatures(columns)(features)
        loss = tf.reduce_mean(out_emb)
        opt = tf.train.GradientDescentOptimizer(lr)
        step = tf.train.get_or_create_global_step()
        train_op = opt.minimize(loss, global_step=step)

        final_loss = None
        with tf.train.MonitoredTrainingSession(
            '',
            hooks=[
              tf.train.StopAtStepHook(last_step=2),
              tf.train.NanTensorHook(loss),
              tf.train.LoggingTensorHook(
                tensors={'loss': loss, 'step': step},
                every_n_iter=20)]) as sess:
          while not sess.should_stop():
            final_loss = sess.run(loss)
            sess.run(train_op)
        return final_loss

  def test_1_col_2_steps(self):
    final_loss = self._test_1_col_2_steps(42, 0.0001)
    np.testing.assert_allclose(final_loss, 0.499999, rtol=1e-6)

  def _test_1_col_2_steps_adam(self, seed, lr):
    with tf.Graph().as_default():
      with hb.scope(
          seed=seed,
          comm_pool_name='test_1_col_2_steps_adam',
          emb_buffer_size=10,
          emb_device='/cpu:0'):
        columns = [
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='ad0', num_buckets=20, default_value=0),
            dimension=20,
            initializer=tf.constant_initializer(0.5)),
        ]
        features = {
          'ad0': tf.constant([0, 1, 3, 2])
        }
        out_emb = tf.keras.layers.DenseFeatures(columns)(features)
        loss = tf.reduce_mean(out_emb)
        opt = tf.train.AdamOptimizer(lr)
        step = tf.train.get_or_create_global_step()
        train_op = opt.minimize(loss, global_step=step)

        final_loss = None
        with tf.train.MonitoredTrainingSession(
            '',
            hooks=[
              tf.train.StopAtStepHook(last_step=2),
              tf.train.NanTensorHook(loss),
              tf.train.LoggingTensorHook(
                tensors={'loss': loss, 'step': step},
                every_n_iter=20)]) as sess:
          while not sess.should_stop():
            final_loss = sess.run(loss)
            sess.run(train_op)
        return final_loss

  def test_1_col_2_steps_adam(self):
    final_loss = self._test_1_col_2_steps_adam(42, 0.0001)
    np.testing.assert_allclose(final_loss, 0.4999, rtol=1e-6)

  def _test_n_cols_n_steps(self, seed, lr):
    with tf.Graph().as_default():
      with hb.scope(
          seed=seed,
          comm_pool_name='test_n_cols_n_steps',
          emb_buffer_size=10,
          emb_device='/cpu:0'):
        columns = [
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='ad0', num_buckets=20, default_value=0),
            dimension=20,
            initializer=tf.constant_initializer(0.5)),
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='ad1', num_buckets=20, default_value=0),
            dimension=30,
            initializer=tf.constant_initializer(0.5)),
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='ad2', num_buckets=20, default_value=0),
            dimension=40,
            initializer=tf.constant_initializer(0.5)),
          fc.embedding_column(
            fc.categorical_column_with_identity(
              key='user0', num_buckets=20, default_value=0),
            dimension=20,
            initializer=tf.constant_initializer(0.5)),
        ]
        features = {
          'ad0': tf.constant([0, 1, 3, 2]),
          'ad1': tf.constant([1, 5, 3, 4]),
          'ad2': tf.constant([5, 2, 7, 4]),
          'user0': tf.constant([2, 5, 4, 7])
        }
        out_emb = tf.keras.layers.DenseFeatures(columns)(features)
        loss = tf.reduce_mean(out_emb)
        opt = tf.train.AdamOptimizer(lr)
        step = tf.train.get_or_create_global_step()
        train_op = opt.minimize(loss, global_step=step)

        final_loss = None
        with tf.train.MonitoredTrainingSession(
            '',
            hooks=[
              tf.train.StopAtStepHook(last_step=100),
              tf.train.NanTensorHook(loss),
              tf.train.LoggingTensorHook(
                tensors={'loss': loss, 'step': step},
                every_n_iter=20)]) as sess:
          while not sess.should_stop():
            final_loss = sess.run(loss)
            sess.run(train_op)
        return final_loss

  def test_n_cols_n_steps(self):
    final_loss = self._test_n_cols_n_steps(42, 0.0001)
    np.testing.assert_allclose(final_loss, 0.490101, rtol=1e-6)


# pylint: enable=missing-docstring
if __name__ == '__main__':
  hbtest.main()
