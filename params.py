#!/usr/bin/env python 
from __future__ import division

import os
from collections import OrderedDict

##########################################################
# camera module selection
#   "camera-webcam" "camera-null"
##########################################################
camera="camera-null"

##########################################################
# actuator selection
#   "actuator-drv8835", "actuator-adafruit_hat"
#   "actuator-null"
##########################################################
actuator="actuator-null"

##########################################################
# model selection
#   "model-5conv_3fc"   <-- nvidia dave-2 model
#   "model-5conv_4fc"   <-- deeptesla model
#
# model checkpoint file selection
#   "model-5conv_3fc_noreuse.ckpt"  <-- ittc building maze
#   "model-5conv_3fc-home_night.ckpt" <-- kitchen@night
##########################################################
model="model-5conv_3fc-200x200"
model_save_file=""
model_load_file="input200x200"

##########################################################
# Training options
##########################################################
batch_size = 100
training_steps = 2000
img_height =200
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

epochs = OrderedDict()
epochs['train'] = [1,3,5,7,9,11] 
epochs['val']   = [2,4,6,8,10]

