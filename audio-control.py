#!/usr/bin/env python

import os
import sys
import time
import tensorflow as tf
import numpy as np
import wave
import alsaaudio
import struct
import array
import wave
import audioop
import params
from pololu_drv8835_rpi import motors,MAX_SPEED

actuator = __import__(params.actuator)
actuator.init()

def write_to_wav(arr):
    wavefile = wave.open("tmp/test.wav", 'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(16000)
    wavefile.writeframes(b''.join(arr))
    wavefile.close()

def read_from_wav():
    wavefile = open("tmp/test.wav", 'rb')
    data = wavefile.read()
    wavefile.close()
    return data

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device="sysdefault:CARD=CameraB409241")
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

input_layer_name = 'wav_data:0'
output_layer_name = 'labels_softmax:0'

f = tf.gfile.GFile("./stopgo_svdf_frozen_graph.pb", 'rb')
l = tf.gfile.GFile("./stopgo_svdf_labels.txt")

config = tf.ConfigProto(intra_op_parallelism_threads=4,
                            inter_op_parallelism_threads=4, \
                            allow_soft_placement=True,
                            device_count = {'CPU': 1})
sess = tf.Session(config=config)

graph_def = tf.GraphDef()
graph_def.ParseFromString(f.read())
tf.import_graph_def(graph_def, name='')

data_dir = os.path.abspath('tmp')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

init = []
for i in range(40000):
    temp,data = inp.read()
    init.append(data)
write_to_wav(b''.join(init))
warmup_data = read_from_wav()
softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
predictions, = sess.run(softmax_tensor, {input_layer_name: warmup_data})

labels = [line.rstrip() for line in l]

times = []
first = True

threshold = 700

print "START"
while True:
    cur = []
    for i in range(15000):
        temp, data = inp.read()
        cur.append(data)
    str = b''.join(cur)
    if audioop.rms(str, 2) > threshold:
        print audioop.rms(str,2)
        arr = []
        arr.append(str)
        for i in range(15000):
            temp, data = inp.read()
            arr.append(data)
        write_to_wav(arr)
        input_data = read_from_wav()

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
            if labels[top] == "go":
                actuator.ffw()
            elif labels[top] == "stop":
                actuator.stop()

print "Num: {}".format(len(times))
print "Average: {}".format(np.mean(times))
