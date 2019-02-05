import params
import time
import zmq
import audioop
import signal

mic = __import__(params.microphone)
mic.init()

context = zmq.Context()
audio_sock = context.socket(zmq.PUB)
audio_sock.bind("tcp://127.0.0.1:5681")

while True:
    cur = []
    for i in range(params.audio_length1):
        temp, data = mic.read()
        cur.append(data)
    str = b''.join(cur)

    if audioop.rms(str, 2) > params.audio_threshold:
        print audioop.rms(str,2)
        arr = []
        arr.append(str)
        for i in range(params.audio_length2):
            temp, data = mic.read()
            arr.append(data)
        audio_sock.send_multipart( ["AUDIO", b''.join(arr)])
