#!/usr/bin/env python
from __future__ import division

import random
import os
import sys
from collections import OrderedDict
import cv2
import params

import local_common as cm

################ parameters ###############
img_height = params.img_height
img_width = params.img_width
img_channels = params.img_channels

def preprocess(img):
    assert img_channels == 3 # for now we expect a color image
    ratio = img_height / img_width
    y1, y2 = 350, 553
    w = (y2-y1) / ratio
    padding = int(round((img.shape[1] - w) / 2))
    # img = img[y1:y2, padding:-padding]
    img = cv2.resize(img, (img_width, img_height))
    img = img / 255.
    return img

