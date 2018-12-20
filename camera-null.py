import time
import numpy as np

use_thread = False
cap = None
frame = None

# public API
# init(), read_frame(), stop()

frame = np.zeros((320,240,3), np.uint8)

def init(res=(320, 240), fps=30, threading=True):
    print ("Initilize NULL camera. (%d x %d)" % (res[0], res[1]))
    print ("camera init completed.")

def read_frame():
    return frame

def stop():
    print ("Close the camera.")
