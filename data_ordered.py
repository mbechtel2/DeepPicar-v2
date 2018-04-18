#!/usr/bin/env python
from __future__ import division

import random
import os
import sys
from collections import OrderedDict
import cv2
import params
import preprocess

import local_common as cm

################ parameters ###############
data_dir = params.data_dir
batch_size = params.batch_size
epochs = params.epochs
img_height = params.img_height
img_width = params.img_width
img_channels = params.img_channels

############### building the batch definitions ###############
purposes = ['train', 'val']
batches = OrderedDict()
for purpose in purposes:
    batches[purpose] = []

# determine the epoch_id, frame_start, frame_end
for purpose in epochs.keys():
    assert len(epochs[purpose]) > 0
    for epoch_id in epochs[purpose]:
        vid_path = cm.jn(data_dir, 'epoch{:0>2}_front.mkv'.format(epoch_id))
        assert os.path.isfile(vid_path)
        frame_count = cm.frame_count(vid_path)
        assert batch_size <= frame_count

        batch_count = int(frame_count / batch_size)
        assert batch_count >= 1
        for b in xrange(batch_count):
            assert purpose in batches
            frame_start = b * batch_size
            frame_end = frame_start + batch_size - 1
            assert frame_end < frame_count
            batches[purpose].append(OrderedDict([
                ('epoch_id', epoch_id),
                ('frame_start', frame_start),
                ('frame_end', frame_end),
            ]))
        
current_batch_id = OrderedDict()
for purpose in purposes:
    current_batch_id[purpose] = 0

def load_batch(purpose):
    global current_batch_id
    xx = []
    yy = []

    # fetch the batch definition
    batch_id = current_batch_id[purpose]
    assert batch_id < len(batches[purpose])
    batch = batches[purpose][batch_id]
    epoch_id, frame_start, frame_end = batch['epoch_id'], batch['frame_start'], batch['frame_end']
    assert epoch_id is not None and frame_start is not None and frame_end is not None

    # update the current batch
    current_batch_id[purpose] = (current_batch_id[purpose] + 1) % len(batches[purpose])

    # fetch image and steering data
    vid_path = cm.jn(data_dir, 'epoch{:0>2}_front.mkv'.format(epoch_id))
    assert os.path.isfile(vid_path)
    frame_count = cm.frame_count(vid_path)
    cap = cv2.VideoCapture(vid_path)
    cm.cv2_goto_frame(cap, frame_start)

    csv_path = cm.jn(data_dir, 'epoch{:0>2}_steering.csv'.format(epoch_id))
    assert os.path.isfile(csv_path)
    rows = cm.fetch_csv_data(csv_path)
    assert frame_count == len(rows)
    yy = [[float(row['wheel'])] for row in rows[frame_start:frame_end+1]]

    for frame_id in xrange(frame_start, frame_end+1):
        ret, img = cap.read()
        assert ret

        img = preprocess.preprocess(img)
        
        #cv2.imwrite(os.path.abspath('output/sample_frame.jpg'), img)            

        xx.append(img)

    assert len(xx) == len(yy)

    cap.release()

    return xx, yy
