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
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding='SAME')

def maxpool2d(x, k, s):
    # MaxPool2D wrapper
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, s, s, 1], padding='SAME')
    
x = tf.placeholder(tf.float32,
                   shape=[None, params.img_height, params.img_width, params.img_channels])
y_ = tf.placeholder(tf.float32, shape=[None, 1])

x_image = x

print ("input: {}".format(x_image.get_shape()))

# first convolutional layer
W_conv1 = weight_variable("wc1", [3, 3, 3, 8])
b_conv1 = bias_variable([8])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1, 3) + b_conv1)
print ("h_conv1: {}".format(h_conv1.get_shape()))

# second convolutional layer
W_conv2 = weight_variable("wc2", [3, 3, 8, 8])
b_conv2 = bias_variable([8])

h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2, 3) + b_conv2)
print ("h_conv2: {}".format(h_conv2.get_shape()))

# third convolutional layer
W_conv3 = weight_variable("wc3", [3, 3, 8, 8])
b_conv3 = bias_variable([8])

h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 3) + b_conv3)
print ("h_conv3: {}".format(h_conv3.get_shape()))

# pooling
h_conv3_pool = tf.nn.relu(maxpool2d(h_conv3, 4, 2))
print ("h_conv3_pool: {}".format(h_conv3_pool.get_shape()))

h_conv3_flat = tf.reshape(h_conv3_pool, [-1, 64])
print ("h_conv3_flat: {}".format(h_conv3_flat.get_shape()))

keep_prob = tf.placeholder(tf.float32)

# output
W_fc5 = weight_variable("fc", [64, 1])
b_fc5 = bias_variable([1])

y = tf.multiply(tf.atan(tf.matmul(h_conv3_flat, W_fc5) + b_fc5), 2) #scale the atan output
