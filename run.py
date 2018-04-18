#!/usr/bin/env python 
from __future__ import division

import tensorflow as tf
import params
model = __import__(params.model)    
import cv2
import subprocess as sp
import itertools
import sys
import os
import preprocess
# import visualize_parallel
import visualize
import time
import math

import local_common as cm

from joblib import Parallel, delayed 
import multiprocessing

# for picar-mini-v2.0
def deg2rad(deg):
        return deg * math.pi / 180.0
def rad2deg(rad):
        return 180.0 * rad / math.pi

sess = tf.InteractiveSession()
saver = tf.train.Saver()
model_load_path = cm.jn(params.save_dir, params.model_load_file)
saver.restore(sess, model_load_path)

epoch_ids = sorted(list(set(itertools.chain(*params.epochs.values()))))

def process_epoch(epoch_id):
    print '---------- processing video for epoch {} ----------'.format(epoch_id)
    vid_path = cm.jn(params.data_dir, 'out-video-{}.avi'.format(epoch_id))
    frame_count = cm.frame_count(vid_path)        
    
    vid_scaled_path = cm.jn(params.data_dir, 'out-video-{}-scaled.avi'.format(epoch_id))
    if not os.path.exists(vid_scaled_path):
        assert os.path.isfile(vid_path)
        os.system("ffmpeg -i " + vid_path + " -vf scale=1280:720 " + vid_scaled_path)
        print("ffmpeg -i " + vid_path + " -vf scale=1280:720 " + vid_scaled_path)
    vid_path = vid_scaled_path
    
    cap = cv2.VideoCapture(vid_path)

    machine_steering = []

    print 'performing inference...'
    time_start = time.time()
    for frame_id in xrange(frame_count):
        ret, img = cap.read()
        assert ret

        prep_start = time.time()
        img = preprocess.preprocess(img)

        pred_start = time.time()
        rad = model.y.eval(feed_dict={model.x: [img], model.keep_prob: 1.0})[0][0]
        deg = rad2deg(rad)
        pred_end   = time.time()

        prep_time = pred_start - prep_start
        pred_time = pred_end - pred_start

        # print 'pred: {} deg. took {} ms'.format(deg, pred_time * 1000)
        # print 'pred: {} deg (rad={})'.format(deg, rad)

        machine_steering.append(deg)

    cap.release()

    fps = frame_count / (time.time() - time_start)
    print ('completed inference, total frames: {}, average fps: {} Hz'.format(frame_count, round(fps, 1)))
    # print "Machine Steering:", machine_steering
    return machine_steering

def visualize_epoch(job):
    epoch_id = job[0]
    machine_steering = job[1]
    visualize.visualize(epoch_id, machine_steering, params.out_dir,
                        verbose=True, frame_count_limit=None)
job_list = []
for epoch_id in epoch_ids:
    steering = process_epoch(epoch_id)
    job_list.append([epoch_id, steering])

print "visualize epochs in parallel"    
num_cores = int(multiprocessing.cpu_count()/2)
Parallel (n_jobs = num_cores) (delayed (visualize_epoch) (job) for job in job_list)

     
