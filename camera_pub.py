import params
import signal
import time
import zmq
import pickle

period = 0.05
cfg_cam_res = (320, 240)
cfg_cam_fps = 30
use_thread=True

def g_tick():
    t = time.time()
    count = 0
    while True:
	count += 1
        yield max(t + count*period - time.time(), 0)

def signal_handler(sig, frame):
    camera.stop()
    quit()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

context = zmq.Context()
frame_sock = context.socket(zmq.PUB)
frame_sock.bind("tcp://127.0.0.1:5680")
frame_sock.setsockopt(zmq.CONFLATE, 1)

camera = __import__(params.camera)
camera.init(res=cfg_cam_res, fps=cfg_cam_fps, threading=use_thread)

g = g_tick()

while True:
    if use_thread:
	time.sleep(next(g))
    frame = camera.read_frame()
    if not frame is None:
	frame_sock.send_multipart(["FRAME", frame, str(frame.dtype)])
