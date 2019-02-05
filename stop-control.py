#!/usr/bin/python
import os
import signal
import sys
import time
import math
import numpy as np
import sys
import params
import argparse
import zmq
import pickle
import local_common as cm
import tensorflow as tf
model = __import__(params.stop_model)
import local_common as cm
import preprocess

#Get user parameters:
#   -n / --ncpu : number of cores used by TensorFlow for inferencing
#   -t / --thres : threshold for determing if the car should stop or go
NCPU = 2
threshold = params.stop_threshold
parser = argparse.ArgumentParser(description='Stoplight recognition control')
parser.add_argument("-n", "--ncpu",
                    help="number of cores to use.", type=int)
parser.add_argument("-t", "--thres",
                    help="stop/go threshold (0-1).", type=float)
args = parser.parse_args()
if args.ncpu > 0:
    NCPU = args.ncpu
if args.thres > 0 and args.thres < 1:
    threshold = args.thres

#Initilize DNN model
config = tf.ConfigProto(intra_op_parallelism_threads=NCPU,
                        inter_op_parallelism_threads=NCPU, \
                        allow_soft_placement=True,
                        device_count = {'CPU': 1})
sess = tf.InteractiveSession(config=config)
saver = tf.train.Saver()
model_load_path = cm.jn(params.save_dir, params.stop_model_load_file)
saver.restore(sess, model_load_path)

#Setup IPC sockets
context = zmq.Context()
stopgo_sock = context.socket(zmq.PUB)
stopgo_sock.connect("tcp://127.0.0.1:5678")

frame_sock = context.socket(zmq.SUB)
frame_sock.connect("tcp://127.0.0.1:5680")
frame_sock.setsockopt_string(zmq.SUBSCRIBE, "FRAME".decode('ascii'))

#Warmup
msg = frame_sock.recv_multipart()
frame = pickle.loads(msg[1])
img = preprocess.preprocess(frame)
angle = model.y.eval(feed_dict={model.x: [img]})[0][0]

tot_time_list = []

#Main image processing loop
while True:
    #1. Get the current camera frame
    msg = frame_sock.recv_multipart()
    frame = pickle.loads(msg[1])
    ts = time.time()

    #2. Preprocess the frame
    img = preprocess.preprocess(frame)

    #3. Feed the preprocessed frame to the model and get the predicted output
    dnn_throttle = model.y.eval(feed_dict={model.x: [img]})[0][0]
    print dnn_throttle

    #4. Send the appropriate message back to the main control loop
    if dnn_throttle < params.stop_threshold:
        stopgo_sock.send_multipart(["STOPGO","stop"])
    else:
        stopgo_sock.send_multipart(["STOPGO","go"])

    dur = time.time() - ts

    tot_time_list.append(dur)

#Calculate and display statistics of the total inferencing times
print "count:", len(tot_time_list)
print "mean:", np.mean(tot_time_list)
print "max:", np.max(tot_time_list)
print "99.999pct:", np.percentile(tot_time_list, 99.999)
print "99.99pct:", np.percentile(tot_time_list, 99.99)
print "99.9pct:", np.percentile(tot_time_list, 99.9)
print "99pct:", np.percentile(tot_time_list, 99)
print "min:", np.min(tot_time_list)
print "median:", np.median(tot_time_list)
print "stdev:", np.std(tot_time_list)
