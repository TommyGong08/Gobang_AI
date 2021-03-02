import tensorflow as tf


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='VALID')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='VALID')


def convolutional_neural_network(input):

    #9*9*2
    W_conv1 = weight_variable([3, 3, 2, 64])
    b_conv1 = bias_variable([64])

    h_conv1 = tf.nn.relu(conv2d(input, W_conv1) + b_conv1)

    #9*9*2
    W_conv2 = weight_variable([4, 4, 64, 128])
    b_conv2 = bias_variable([128])

    h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)

    #9*9*2
    W_conv3 = weight_variable([5, 5, 128, 128])
    b_conv3 = bias_variable([128])

    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3) + b_conv3)

    #9*9*2
    W_conv4 = weight_variable([5, 5, 128, 256])
    b_conv4 = bias_variable([256])

    h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4) + b_conv4)

    h_pool1_flat = tf.reshape(h_conv4, [-1, 2 * 2 * 256])

    #2*2*128
    W_fc1 = weight_variable([2 * 2 * 256, 128])
    b_fc1 = bias_variable([128])

    h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)

    #2*2*128
    W_fc2 = weight_variable([128, 32])
    b_fc2 = bias_variable([32])

    h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)

    #2*2*128
    W_fc3 = weight_variable([32, 2])
    b_fc3 = bias_variable([2])

    h_fc3 = tf.nn.softmax(tf.matmul(h_fc2, W_fc3) + b_fc3)

    return h_fc3


