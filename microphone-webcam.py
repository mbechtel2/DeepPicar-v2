import params
import alsaaudio
import wave

def write_to_wav(arr):
    wavefile = wave.open(params.audio_input_data_file, 'wb')
    wavefile.setnchannels(params.audio_channels)
    wavefile.setsampwidth(params.audio_sampwidth)
    wavefile.setframerate(params.audio_rate)
    wavefile.writeframes(b''.join(arr))
    wavefile.close()

def read_from_wav():
    wavefile = open(params.audio_input_data_file, 'rb')
    data = wavefile.read()
    wavefile.close()
    return data

inp = None

def init():
    global inp
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, device=params.audio_device)
    inp.setchannels(params.audio_channels)
    inp.setrate(params.audio_rate)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(params.audio_period)

def read():
    global inp
    return inp.read()
