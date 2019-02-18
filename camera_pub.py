import params
import signal
import time
import zmq
import pickle
import rospy
from std_msgs.msg import *
from sensor_msgs.msg import *
from cv_bridge import CvBridge

period = 0.05
cfg_cam_res = (320, 240)
cfg_cam_fps = 30
use_thread=True

def signal_handler(sig, frame):
    camera.stop()
    quit()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

'''
context = zmq.Context()
frame_sock = context.socket(zmq.PUB)
frame_sock.bind("tcp://127.0.0.1:5680")
'''

camera = __import__(params.camera)
camera.init(res=cfg_cam_res, fps=cfg_cam_fps, threading=use_thread)
bridge = CvBridge()
frame_pub = rospy.Publisher('FRAME', Image, queue_size=10)
rospy.init_node('FramePub', anonymous=True)
rate = rospy.Rate(10)
while True:
    frame = camera.read_frame()
    if not frame is None:
        img = bridge.cv2_to_imgmsg(frame) #, "bgr8")
        frame_pub.publish(img)
        rate.sleep()
    #frame_sock.send_multipart( ["FRAME", pickle.dumps(frame)])
