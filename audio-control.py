#!/usr/bin/env python

import os
import sys
import time
import tensorflow as tf
import numpy as np
import argparse
import alsaaudio
import wave
import audioop
import params
import zmq

mic = __import__(params.microphone)

#Get user parameters:
#   -n / --ncpu : number of cores used by TensorFlow for inferencing
#   -t / --thres : threshold for determing if a sound should be processed
NCPU = 2
threshold = 500
first = True
times = []
parser = argparse.ArgumentParser(description='Voice control')
parser.add_argument("-n", "--ncpu",
                    help="number of cores to use.", type=int)
parser.add_argument("-t", "--thres",
                    help="audio processing threshold.", type=float)
args = parser.parse_args()
if args.ncpu > 0:
    NCPU = args.ncpu
if args.thres > 0:
    threshold = args.thres

#Setup DNN model
f = tf.gfile.GFile(params.audio_model_load_file, 'rb')
l = tf.gfile.GFile(params.audio_label_load_file)
input_layer_name = 'wav_data:0'
output_layer_name = 'labels_softmax:0'
labels = [line.rstrip() for line in l]
config = tf.ConfigProto(intra_op_parallelism_threads=NCPU,
                            inter_op_parallelism_threads=NCPU, \
                            allow_soft_placement=True,
                            device_count = {'CPU': 1})
sess = tf.Session(config=config)
graph_def = tf.GraphDef()
graph_def.ParseFromString(f.read())
tf.import_graph_def(graph_def, name='')

#If needed, create directory for storing DNN input data
data_dir = os.path.abspath('tmp')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

#Setup IPC sockets
context = zmq.Context()
stopgo_sock = context.socket(zmq.PUB)
stopgo_sock.connect("tcp://127.0.0.1:5678")

audio_sock = context.socket(zmq.SUB)
audio_sock.connect("tcp://127.0.0.1:5681")
audio_sock.setsockopt_string(zmq.SUBSCRIBE, "AUDIO".decode('ascii'))

#Warmup
init = audio_sock.recv_multipart()[1]
mic.write_to_wav(init)
warmup_data = mic.read_from_wav()
softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
predictions, = sess.run(softmax_tensor, {input_layer_name: warmup_data})

#Main audio processing loop
while True:
    arr = audio_sock.recv_multipart()[1]
    mic.write_to_wav(arr)

    input_data = mic.read_from_wav()
    start = time.time()
    softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
    predictions, = sess.run(softmax_tensor, {input_layer_name: input_data})
    end = time.time()
    dur = (end - start) * 1000
    print dur
    top = predictions.argsort()[-1:][::-1][0]
    word = labels[top]
    val = predictions[top]
    print "\t{} w/ {}".format(word, val)
    times.append(dur)

    if first:
        first = False
    else:
        if labels[top] == "go" or labels[top] == "stop":
            print labels[top]
            sock.send_multipart( ["STOPGO", labels[top]] )

print "Num: {}".format(len(times))
print "Average: {}".format(np.mean(times))
