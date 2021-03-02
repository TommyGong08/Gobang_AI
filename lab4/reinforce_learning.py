#!/usr/bin/env python

import tensorflow as tf
import net

history_data = []

train_data = {"x": [], "y": []}
sess = tf.Session()
x = tf.placeholder(tf.float32, [None, 15, 15, 2])
y_ = tf.placeholder("float", shape=[None, 2])

x_board = tf.reshape(x, [-1, 15, 15, 2])
y_conv = net.convolutional_neural_network(x_board)

# cost = -tf.reduce_sum(tf.square(y_ - y_conv))
cost = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-3).minimize(cost)

sess.run(tf.initialize_all_variables())


def train():
    for i in range(50):
        if i % 10 == 0:
            print("step %d " % (i, ))
        sess.run(train_step, feed_dict={x: train_data['x'], y_: train_data['y']})


def get_value(board):
    board2 = [board, ]
    value = sess.run(y_conv, feed_dict={x: board2})
    return value[0][0]


