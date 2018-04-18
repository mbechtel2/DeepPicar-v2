import serial

cur_speed = 0

# init
def init(default_speed=50):
    global ser
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    stop()
    set_speed(default_speed)
    print ("actuator-arduino init completed.")

def set_speed(speed):
    global cur_speed
    ser.write("t " + str(speed))
    cur_speed = speed
    
def get_speed():
    return cur_speed

def stop():
    ser.write("s\n")
        
def ffw():
    ser.write("a\n")    

def rew():
    ser.write("z\n")        

# steering
def center():
    ser.write("k\n")    
def left():
    ser.write("j\n")
def right():
    ser.write("l\n")    

# exit    
def turn_off():
    stop()
    center()
    ser.close()
