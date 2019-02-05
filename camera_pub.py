import params
import signal
import time
import zmq
import pickle

period = 0.05
cfg_cam_res = (320, 240)
cfg_cam_fps = 30
use_thread=True

def signal_handler(sig, frame):
    camera.stop()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

context = zmq.Context()
frame_sock = context.socket(zmq.PUB)
frame_sock.bind("tcp://127.0.0.1:5680")

camera = __import__(params.camera)
camera.init(res=cfg_cam_res, fps=cfg_cam_fps, threading=use_thread)

while True:
    frame = camera.read_frame()
    frame_sock.send_multipart( ["FRAME", pickle.dumps(frame)])
