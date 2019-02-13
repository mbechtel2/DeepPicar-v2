#!/usr/bin/env python
from __future__ import division

import os
from collections import OrderedDict

##########################################################
# camera module selection
#   "camera-webcam" "camera-null"
##########################################################
camera="camera-webcam"

##########################################################
# actuator selection
#   "actuator-drv8835", "actuator-adafruit_hat"
#   "actuator-null"
##########################################################
actuator="actuator-drv8835"

##########################################################
# microphone module selection
#   "microphone-webcam" "microphone-null"
##########################################################
microphone="microphone-webcam"

audio_device = "sysdefault:CARD=CameraB409241"
audio_channels = 1
audio_sampwidth = 2
audio_rate = 16000
audio_period = 160
audio_length1 = 20000
audio_length2 = 80000
audio_threshold = 700

##########################################################
# model selection
#   "model-5conv_3fc"   <-- nvidia dave-2 model
#   "model-5conv_4fc"   <-- deeptesla model
#
# model checkpoint file selection
#   "model-5conv_3fc_noreuse.ckpt"  <-- ittc building maze
#   "model-5conv_3fc-home_night.ckpt" <-- kitchen@night
##########################################################
model="model-3conv_1pool"
model_load_file="DeepPicar-rlgl.ckpt"
model_load_file2="model-5conv_3fc-home_night.ckpt"
model_load_file3="model-5conv_3fc-home_night.ckpt"
model_load_file4="model-5conv_3fc-home_night.ckpt"
model_save_file=model_load_file

stop_model="model-stop-3conv_1pool"
stop_model_load_file = "DeepPicar-stop-all-normal-4000.ckpt"
stop_model_save_file = stop_model_load_file
stop_threshold = 0.5

audio_model_load_file = "audio-models/svdf_frozen_graph.pb"
audio_label_load_file = "audio-models/svdf_labels.txt"
audio_input_data_file = "tmp/test.wav"

##########################################################
# Training options
##########################################################
batch_size = 100
training_steps = 4000
img_height = 66
img_width = 200
img_channels = 3
write_summary = True
shuffle_training = True
use_category_normal = True # if ture, center/curve images
                           # are equally selected.
use_picar_mini = True # visualization fix for picar mini

##########################################################
# Directories
##########################################################
save_dir = os.path.abspath('models')
data_dir = os.path.abspath('epochs')
out_dir = os.path.abspath('output')

if not os.path.isdir(data_dir):
    os.makedirs(data_dir)
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

all = [2,3,4,7,8,9,10,11,12,13,14,15,20,21,22,23]

epochs = OrderedDict()
epochs['train'] = all#[2,3,5,8,10,20,12,14,22]
epochs['val']   = all#[4,6,7,9,11,21,13,15,23]
