from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

# init
mh = Adafruit_MotorHAT(addr=0x60)

# throttle
cur_speed = 0
MAX_SPEED = 255

# Actuator API:
#   init, stop, set/get_speed, ffw, rew, left, right, center
def init(default_speed=50):
    global steering, throttle
    steering = mh.getMotor(1)
    throttle = mh.getMotor(2)
    set_speed(default_speed)
    
def set_speed(speed):
    global cur_speed
    speed = int(MAX_SPEED * speed / 100)
    cur_speed = min(MAX_SPEED, speed)
    print ("speed: %d" % cur_speed)

def get_speed():
    return int(cur_speed * 100 / MAX_SPEED)

def ffw():
    throttle.setSpeed(cur_speed)    
    throttle.run(Adafruit_MotorHAT.FORWARD)    

def rew():
    throttle.setSpeed(cur_speed)    
    throttle.run(Adafruit_MotorHAT.BACKWARD)

# steering
def center():
    steering.setSpeed(0)
def left():
    steering.setSpeed(MAX_SPEED)
    steering.run(Adafruit_MotorHAT.BACKWARD)        
def right():
    steering.setSpeed(MAX_SPEED)
    steering.run(Adafruit_MotorHAT.FORWARD)

# stop    
def stop():
    throttle.setSpeed(0)
    steering.setSpeed(0)
    throttle.run(Adafruit_MotorHAT.RELEASE)
    steering.run(Adafruit_MotorHAT.RELEASE)
    
