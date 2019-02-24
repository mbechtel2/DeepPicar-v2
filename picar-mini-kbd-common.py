#!/usr/bin/python
import os
import signal
import sys
import time
import atexit
import cv2
import math
import numpy as np
import sys
import params
import argparse

import Image
import ImageDraw
import local_common as cm

import input_kbd

##########################################################
# import deeppicar's sensor/actuator modules
##########################################################
camera   = __import__(params.camera)
actuator = __import__(params.actuator)

##########################################################
# global variable initialization
##########################################################
use_dnn = False
use_thread = True
use_keyinput = True
view_video = False
fpv_video = False

cfg_cam_res = (320, 240)
cfg_cam_fps = 30
cfg_throttle = 50 # 50% power.

NCPU = 2

frame_id = 0
angle = 0.0
btn   = ord('k') # center
period = 0.05 # sec (=50ms)
timeout = 0.0 # no timeout
tot_time_list = []

##########################################################
# local functions
##########################################################
def deg2rad(deg):
    return deg * math.pi / 180.0
def rad2deg(rad):
    return 180.0 * rad / math.pi

def g_tick():
    t = time.time()
    count = 0
    while True:
        count += 1
        yield max(t + count*period - time.time(),0)

def turn_off():
    actuator.stop()
    camera.stop()

    keyfile.close()
    keyfile_btn.close()
    vidfile.release()

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

def signal_handler(sig, frame):
    turn_off()
    sys.exit(0)

##########################################################
# program begins
##########################################################
parser = argparse.ArgumentParser(description='DeepPicar main')
parser.add_argument("-d", "--dnn",
                    help="Enable DNN", action="store_true")
parser.add_argument("-t", "--throttle",
                    help="throttle percent. [0-100]%", type=int)
parser.add_argument("-n", "--ncpu",
                    help="number of cores to use.", type=int)
parser.add_argument("-f", "--fpvvideo",
                    help="Take FPV video of DNN driving", action="store_true")
parser.add_argument("-x", "--time",
                    help="exit time limit in seconds.", type=int)
parser.add_argument("-p", "--period",
                    help="real-time control period in ms.", type=float)
parser.add_argument("-k", "--nokey",
                    help="no keyboard input mode", action="store_true")
parser.add_argument("-v", "--verbose",
                    help="debug level", type=int)

args = parser.parse_args()

if args.dnn:
    print ("DNN is on")
    use_dnn = True
if args.throttle:
    cfg_throttle = args.throttle
    print ("throttle = %d pct" % (args.throttle))
if args.ncpu > 0:
    NCPU = args.ncpu
if args.fpvvideo:
    fpv_video = True
if args.period:
    period = args.period
    print ("period = %d ms" % int(args.period*1000))
if args.time:
    timeout = args.time
    print ("timeout = %d" % args.time)
if args.nokey:
    use_keyinput = False

# create files for data recording
keyfile = open('out-key.csv', 'w+')
keyfile_btn = open('out-key-btn.csv', 'w+')
keyfile.write("ts_micro,frame,wheel\n")
keyfile_btn.write("ts_micro,frame,btn,speed\n")
rec_start_time = 0
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC(*'XVID')
vidfile = cv2.VideoWriter('out-video.avi', fourcc,
                          cfg_cam_fps, cfg_cam_res)
fpvfile = cv2.VideoWriter('fpv-video.avi', fourcc,
                          cfg_cam_fps, cfg_cam_res)

# initlaize deeppicar modules
actuator.init(cfg_throttle)
camera.init(res=cfg_cam_res, fps=cfg_cam_fps, threading=use_thread)
atexit.register(turn_off)

# initilize dnn model
if use_dnn == True:
    print ("Load TF")
    import tensorflow as tf
    model = __import__(params.model)
    import local_common as cm
    import preprocess

    print ("Load Model")
    config = tf.ConfigProto(intra_op_parallelism_threads=NCPU,
                            inter_op_parallelism_threads=NCPU, \
                            allow_soft_placement=True,
                            device_count = {'CPU': 1})

    sess = tf.InteractiveSession(config=config)
    saver = tf.train.Saver()
    model_load_path = cm.jn(params.save_dir, params.model_load_file)
    saver.restore(sess, model_load_path)

    # warm up.
    frame = camera.read_frame()
    img = preprocess.preprocess(frame)
    angle = model.y.eval(feed_dict={model.x: [img]})[0][0]
    
    print ("Done..")

# null_frame = np.zeros((cfg_cam_res[0],cfg_cam_res[1],3), np.uint8)
# cv2.imshow('frame', null_frame)

g = g_tick()
start_ts = time.time()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# enter main loop
while True:
    if use_thread:
        time.sleep(next(g))
    frame = camera.read_frame()
    ts = time.time()

    # read a frame
    # ret, frame = cap.read()

    if view_video == True:
        cv2.imshow('frame', frame)
        ch = cv2.waitKey(1) & 0xFF
    elif use_keyinput == True:
        ch = ord(input_kbd.read_single_keypress())
    else:
        ch = ''
        
    if ch == ord('j'):
        actuator.left()
        print ("left")
        angle = deg2rad(-30)
        btn   = ord('j')
    elif ch == ord('k'):
        actuator.center()
        print ("center")
        angle = deg2rad(0)
        btn   = ord('k')
    elif ch == ord('l'):
        actuator.right()
        print ("right")
        angle = deg2rad(30)
        btn   = ord('l')
    elif ch == ord('a'):
        actuator.ffw()
        print ("accel")
    elif ch == ord('s'):
        actuator.stop()
        print ("stop")
        btn   = ch
    elif ch == ord('z'):
        actuator.rew()
        print ("reverse")
    elif ch == ord('q'):
        break
    elif ch == ord('r'):
        print ("toggle record mode")
        if rec_start_time == 0:
            rec_start_time = ts
        else:
            rec_start_time = 0
    elif ch == ord('t'):
        print ("toggle video mode")
        if view_video == False:
            view_video = True
        else:
            view_video = False
    elif ch == ord('d'):
        print ("toggle DNN mode")
        if use_dnn == False:
            use_dnn = True
        else:
            use_dnn = False

    if use_dnn == True:
        # 1. machine input
        img = preprocess.preprocess(frame)
        angle = model.y.eval(feed_dict={model.x: [img]})[0][0]
        car_angle = 0

        degree = rad2deg(angle)
        if degree < 15 and degree > -15:
            actuator.center()
            car_angle = 0
            btn = ord('k')
        elif degree >= 15:
            actuator.right()
            car_angle = 30
            btn = ord('l')
        elif degree <= -15:
            actuator.left()
            car_angle = -30
            btn = ord('j')

    dur = time.time() - ts

    tot_time_list.append(dur)
    
    if dur > period:
        print("%.3f: took %.3f ms - deadline miss."
              % (ts - start_ts, float(dur * 1000)))
    elif args.verbose:
        print("%.3f: took %.3f ms" % (ts - start_ts, float(dur * 1000)))

    if rec_start_time > 0:
        # increase frame_id
        frame_id += 1

        # write input (angle)
        str = "{},{},{}\n".format(int(ts*1000), frame_id, angle)
        keyfile.write(str)

        # write input (button: left, center, stop, speed)
        str = "{},{},{},{}\n".format(int(ts*1000), frame_id, btn, cfg_throttle)
        keyfile_btn.write(str)

        if use_dnn and fpv_video:
            textColor = (255,255,255)
            bgColor = (0,0,0)
            newImage = Image.new('RGBA', (100, 20), bgColor)
            drawer = ImageDraw.Draw(newImage)
            drawer.text((0, 0), "Frame #{}".format(frame_id), fill=textColor)
            drawer.text((0, 10), "Angle:{}".format(car_angle), fill=textColor)
            newImage = cv2.cvtColor(np.array(newImage), cv2.COLOR_BGR2RGBA)
            frame = cm.overlay_image(frame,
                                     newImage,
                                     x_offset = 0, y_offset = 0)
        # write video stream
        vidfile.write(frame)
        if frame_id >= 1000:
            print ("recorded 1000 frames")
            break
        print ("%.3f %d %.3f %d %d(ms)" %
           (ts, frame_id, angle, btn, int((time.time() - ts)*1000)))

    if timeout > 0 and (ts - start_ts) > timeout:
        print("timeout after %d seconds" % args.time)
        break
    
print ("Finish..")
turn_off()

