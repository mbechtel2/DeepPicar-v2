import time
import numpy as np
import params

channels = None
rate = None
period = None

arr = []
for i in range(params.audio_length):
    arr.append("")
data = b''.join(arr)

def write_to_wav(arr):
    wavefile = wave.open("tmp/test.wav", 'wb')
    wavefile.setnchannels(1)
    wavefile.setsampwidth(2)
    wavefile.setframerate(16000)
    wavefile.writeframes(b''.join(arr))
    wavefile.close()

def read_from_wav():
    wavefile = open("tmp/test.wav", 'rb')
    data = wavefile.read()
    wavefile.close()
    return data

def init(channels=channels, rate=rate, period=period):
    print ("Initilize NULL microphone.")
    print ("camera init completed.")

def read():
    return data

def stop():
    print ("Close the camera.")
