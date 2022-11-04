#!/usr/bin/python
import os
import time
import atexit
import cv2
import math
import numpy as np
import sys
import params
import argparse

import input_kbd

import pygame
from pygame.locals import *

endProg = False

##########################################################
# Initialize the joystick components
##########################################################
pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()

if joystick_count < 1:
    print("No joysticks found.")
    sys.exit()

print("Found " + str(joystick_count) + " joysticks.")

joy = pygame.joystick.Joystick(0)
joy.init()

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
view_video = False

cfg_cam_res = (320, 240)
cfg_cam_fps = 30
cfg_throttle = 100 # 50% power.

NCPU = 3

frame_id = 0
angle = 0.0
btn   = ord('k') # center
period = 0.05 # sec (=50ms)

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

##########################################################
# program begins
##########################################################
parser = argparse.ArgumentParser(description='DeepPicar main')
parser.add_argument("-d", "--dnn", help="Enable DNN", action="store_true")
parser.add_argument("-t", "--throttle", help="throttle percent. [0-100]%", type=int)
parser.add_argument("-n", "--ncpu", help="number of cores to use.", type=int)
args = parser.parse_args()

if args.dnn:
    print ("DNN is on")
    use_dnn = True
if args.throttle:
    cfg_throttle = args.throttle
    print ("throttle = %d pct" % (args.throttle))
if args.ncpu > 0:
    NCPU = args.ncpu

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
    print ("Done..")

# null_frame = np.zeros((cfg_cam_res[0],cfg_cam_res[1],3), np.uint8)
# cv2.imshow('frame', null_frame)

g = g_tick()
start_ts = time.time()

# enter main loop
while not endProg:
    try:
        #timeStart = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endProg = True
    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            endProg = True

        #throttle = round(joy.get_axis(1)*100, 0)
        #degree = int(joy.get_axis(0)*50)
        #angle = deg2rad(degree)
        endProg = joy.get_button(0)

#        actuator.ffw(throttle)

        if use_thread:
            time.sleep(next(g))
        frame = camera.read_frame()
        ts = time.time()

        # read a frame
        # ret, frame = cap.read()
        
        if view_video == True:
            cv2.imshow('frame', frame)
            ch = cv2.waitKey(1) & 0xFF
        else:
            ch = ord(input_kbd.read_single_keypress())
        
        if ch == ord('j') or joy.get_button(4):
            actuator.left()
            print ("left")
            angle = deg2rad(-30)
            btn   = ord('j')
        elif ch == ord('k'):
            actuator.center()
            print ("center")
            angle = deg2rad(0)
            btn   = ord('k')
        elif ch == ord('l') or joy.get_button(5):
            actuator.right()
            print ("right")
            angle = deg2rad(30)
            btn   = ord('l')
        elif ch == ord('a') or joy.get_button(2):
            actuator.ffw(cfg_throttle)
            print ("accel")
        elif ch == ord('s') or joy.get_button(3):
            actuator.stop()
            print ("stop")
            btn   = ch
        elif ch == ord('z') or joy.get_button(9):
            actuator.rew(cfg_throttle)
            print ("reverse")
        elif ch == ord('q') or joy.get_button(0):
            endProg = True
        elif ch == ord('r') or joy.get_button(1):
            print ("toggle record mode")
            if rec_start_time == 0:
                rec_start_time = ts
            else:
                rec_start_time = 0
        elif ch == ord('t') or joy.get_button(8):
            print ("toggle video mode")
            if view_video == False:
                view_video = True
            else:
                view_video = False
                cv2.destroyAllWindows()
        elif ch == ord('d') or joy.get_button(10):
            print ("toggle DNN mode")
            if use_dnn == False:
                use_dnn = True
            else:
                use_dnn = False

        if use_dnn == True:
            # 1. machine input
            img = preprocess.preprocess(frame)
            angle = model.y.eval(feed_dict={model.x: [img]})[0][0]
            
            degree = int(rad2deg(angle))
            if degree < 1 and degree > -1:
                degree = 0
            elif degree >= 50:
                degree = 50
            elif degree <= -50:
                degree = -50

        actuator.turn(degree)
        #print degree

        dur = time.time() - ts
        if dur > period:
            print("%.3f: took %d ms - deadline miss."
                  % (ts - start_ts, int(dur * 1000)))
        else:
            print("%.3f: took %d ms" % (ts - start_ts, int(dur * 1000)))

        if rec_start_time > 0:
            # increase frame_id
            frame_id += 1
            
            # write input (angle)
            str = "{},{},{}\n".format(int(ts*1000), frame_id, angle)
            keyfile.write(str)
            
            # write input (button: left, center, stop, speed)
            str = "{},{},{},{}\n".format(int(ts*1000), frame_id, btn, cfg_throttle)
            keyfile_btn.write(str)
            
            # write video stream
            vidfile.write(frame)
            
            if frame_id >= 1000:
                print ("recorded 1000 frames")
                break

            print ("%.3f %d %.3f %d %d(ms)" %
               (ts, frame_id, angle, btn, int((time.time() - ts)*1000)))

            #timeEnd = pygame.time.get_ticks()
            #deltaTime = timeEnd - timeStart
            #pygame.time.delay(max(0, 50 - deltaTime))
                
    except KeyboardInterrupt:
        endProg = True
        break

pygame.quit()
turn_off()
print ("Finish..")
