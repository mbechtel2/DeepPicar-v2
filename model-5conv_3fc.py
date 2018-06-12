#!/usr/bin/env python
from __future__ import division

import tensorflow as tf
import params

def weight_variable(name, shape):
    return tf.get_variable(name, shape=shape, initializer=tf.contrib.layers.xavier_initializer())
    # initial = tf.truncated_normal(shape, stddev=0.1)
    # return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding='VALID')

x = tf.placeholder(tf.float32, shape=[None, params.img_height, params.img_width, params.img_channels], name="input_x")
y_ = tf.placeholder(tf.float32, shape=[None, 1])

x_image = x

# first convolutional layer
W_conv1 = weight_variable("wc1", [5, 5, 3, 24])
b_conv1 = bias_variable([24])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1, 2) + b_conv1, name="relu1")

# second convolutional layer
W_conv2 = weight_variable("wc2", [5, 5, 24, 36])
b_conv2 = bias_variable([36])

h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2, 2) + b_conv2, name="relu2")

# third convolutional layer
W_conv3 = weight_variable("wc3", [5, 5, 36, 48])
b_conv3 = bias_variable([48])

h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 2) + b_conv3, name="relu3")

# fourth convolutional layer
W_conv4 = weight_variable("wc4", [3, 3, 48, 64])
b_conv4 = bias_variable([64])

h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4, 1) + b_conv4, name="relu4")

# fifth convolutional layer
W_conv5 = weight_variable("wc5", [3, 3, 64, 64])
b_conv5 = bias_variable([64])

h_conv5 = tf.nn.relu(conv2d(h_conv4, W_conv5, 1) + b_conv5, name="relu5")
h_conv5_flat = tf.reshape(h_conv5, [-1, 1152], name="reshape1")

# fully connected layer 2
W_fc2 = weight_variable("fc2", [1152, 100])
b_fc2 = bias_variable([100])

h_fc2 = tf.nn.relu(tf.matmul(h_conv5_flat, W_fc2, name="matmul1") + b_fc2, name="relu6")

# fully connected layer 3
W_fc3 = weight_variable("fc3", [100, 50])
b_fc3 = bias_variable([50])

h_fc3 = tf.nn.relu(tf.matmul(h_fc2, W_fc3, name="matmul2") + b_fc3, name="relu7")

# fully connected layer 4
W_fc4 = weight_variable("fc4", [50, 10])
b_fc4 = bias_variable([10])

h_fc4 = tf.nn.relu(tf.matmul(h_fc3, W_fc4, name="matmul3") + b_fc4, name="relu8")

# output
W_fc5 = weight_variable("fc5", [10, 1])
b_fc5 = bias_variable([1])

y = tf.multiply(tf.atan(tf.matmul(h_fc4, W_fc5, name="matmul4") + b_fc5), 2, name="atan1") #scale the atan output
