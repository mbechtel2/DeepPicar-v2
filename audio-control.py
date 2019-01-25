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
from pololu_drv8835_rpi import motors,MAX_SPEED

actuator = __import__(params.actuator)
actuator.init()

def write_to_wav(arr):
    wavefile = wave.open("test.wav", 'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(16000)
    wavefile.writeframes(b''.join(arr))
    wavefile.close()

def read_from_wav():
    wavefile = open("test.wav", 'rb')
    data = wavefile.read()
    wavefile.close()
    return data

def convert_to_wav(arr, rate):
    byte_count = (len(arr))  # 32-bit floats
    wav_file = ""
    # write the header
    wav_file += struct.pack('<4sL4s4sLHHLLHH4sL',
        'RIFF', byte_count + 36,  # header size
        'WAVE', 'fmt ',
        16, 1, 1, rate, rate * 2, 2, 16, 'data', byte_count)  # bits / sample
    wav_file+=b''.join(arr)
    return wav_file

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device="sysdefault:CARD=CameraB409241")
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)

input_layer_name = 'wav_data:0'
output_layer_name = 'labels_softmax:0'

f = tf.gfile.GFile("./svdf_frozen_graph.pb", 'rb')
l = tf.gfile.GFile("./svdf_labels.txt")

config = tf.ConfigProto(intra_op_parallelism_threads=4,
                            inter_op_parallelism_threads=4, \
                            allow_soft_placement=True,
                            device_count = {'CPU': 1})
sess = tf.Session(config=config)

graph_def = tf.GraphDef()
graph_def.ParseFromString(f.read())
tf.import_graph_def(graph_def, name='')

labels = [line.rstrip() for line in l]

times = []
first = True

threshold = 1000

print "START"
while True:
    temp, data = inp.read()
    if audioop.rms(data, 2) > threshold:
        print audioop.rms(data,2)
        arr = []
        arr.append(data)
        for i in range(200000):
            temp, data = inp.read()
            arr.append(data)
        #wav_data = convert_to_wav(arr, framerate)
        write_to_wav(arr)

        input_data = read_from_wav()

        start = time.time()
        softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
        predictions, = sess.run(softmax_tensor, {input_layer_name: input_data})
        end = time.time()
        dur = (end - start) * 1000
        print dur
        top = predictions.argsort()[-1:][::-1]
        for i in top:
            word = labels[i]
            val = predictions[i]
            print "\t{} w/ {}".format(word, val)
            if labels[i] == "go" or labels[i] == "no":
                actuator.ffw()
            else if labels[i] == "stop" or labels[i] == "up":
                actuator.stop()
        if first:
            first = False
        else:
            times.append(dur)

print "Num: {}".format(len(times))
print "Average: {}".format(np.mean(times))
