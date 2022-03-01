import cv2
from threading import Thread,Lock
import time

use_thread = False
cap = None
frame = None

# public API
# init(), read_frame(), stop()

def init(res=(320, 240), fps=30, threading=True):
    print ("Initilize camera.")
    global cap, use_thread, frame, cam_thr

    cap = cv2.VideoCapture(0)

    cap.set(3, res[0]) # width
    cap.set(4, res[1]) # height
    cap.set(5, fps)

    # start the camera thread
    if threading:
        use_thread = True
        cam_thr = Thread(target=__update, args=())
        cam_thr.start()
        print ("start camera thread")
        time.sleep(1.0)
    else:
        print ("No camera threading.")

    print ("camera init completed.")

def __update():
    global frame
    while use_thread:
        ret, frame = cap.read() # blocking read
    print ("Camera thread finished...")
    cap.release()        

def read_frame():
    global frame
    if not use_thread:
       ret, frame = cap.read() # blocking read
    return frame

def stop():
    global use_thread
    print ("Close the camera.")
    use_thread = False
