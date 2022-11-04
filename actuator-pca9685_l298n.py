#!/usr/bin/env python
import RPi.GPIO as GPIO
import PCA9685 as p
import time    # Import necessary modules

def Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# ===========================================================================
# Raspberry Pi pin11, 12, 13 and 15 to realize the clockwise/counterclockwise
# rotation and forward and backward movements
# ===========================================================================
Motor0_A = 11  # pin11
Motor0_B = 12  # pin12
Motor1_A = 13  # pin13
Motor1_B = 15  # pin15

# ===========================================================================
# Set channel 4 and 5 of the servo driver IC to generate PWM, thus 
# controlling the speed of the car
# ===========================================================================
EN_M0    = 4  # servo driver IC CH4
EN_M1    = 5  # servo driver IC CH5

pins = [Motor0_A, Motor0_B, Motor1_A, Motor1_B]

def setup(busnum=None):
    global leftPWM, rightPWM, homePWM
    leftPWM = 450
    homePWM = 750
    rightPWM = 1050
    offset =0
    leftPWM += offset
    homePWM += offset
    rightPWM += offset
    
    global forward0, forward1, backward1, backward0, pwm
    if busnum == None:
    	pwm = p.PWM()                  # Initialize the servo controller.
    else:
    	pwm = p.PWM(bus_number=busnum) # Initialize the servo controller.
    
    pwm.frequency = 60
    forward0 = 'True'
    forward1 = 'True'
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)        # Number GPIOs by its physical location
    
    if forward0 == 'True':
    	backward0 = 'False'
    elif forward0 == 'False':
    	backward0 = 'True'
    if forward1 == 'True':
    	backward1 = 'False'
    elif forward1 == 'False':
    	backward1 = 'True'
    for pin in pins:
    	GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode as output


# ===========================================================================
# Control the DC motor to make it rotate clockwise, so the car will
# move forward.
# ===========================================================================

def motor0(x):
    if x == 'True':
        GPIO.output(Motor0_A, GPIO.LOW)
        GPIO.output(Motor0_B, GPIO.HIGH)
    elif x == 'False':
        GPIO.output(Motor0_A, GPIO.HIGH)
        GPIO.output(Motor0_B, GPIO.LOW)
    else:
        print 'Config Error'

def motor1(x):
    if x == 'True':
        GPIO.output(Motor1_A, GPIO.LOW)
        GPIO.output(Motor1_B, GPIO.HIGH)
    elif x == 'False':
        GPIO.output(Motor1_A, GPIO.HIGH)
        GPIO.output(Motor1_B, GPIO.LOW)

# init
def init(default_speed=50):
    setup()
    set_speed(default_speed)

# throttle
cur_speed = 0
MAX_SPEED = 100

def set_speed(speed):
    global cur_speed
    speed = int(MAX_SPEED * speed / 100)
    cur_speed = min(MAX_SPEED, speed)
    speed *= 40
    print 'speed is: ', cur_speed
    pwm.write(EN_M0, 0, speed)
    pwm.write(EN_M1, 0, speed)

def get_speed():
    return int(cur_speed * 100 / MAX_SPEED)

def stop():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

def ffw(spd = 100):
    if spd > 0:
        motor0(forward0)
        motor1(forward1)
    if spd < 0:
        motor0(backward0)
        motor1(backward1)
        spd = -spd
    set_speed(spd)

def rew(spd = 100):
    if spd > 0:
        motor0(backward0)
        motor1(backward1)
    if spd < 0:
        motor0(forward0)
        motor1(forward1)
        spd = -spd
    set_speed(spd)

#def ffw(spd = 50):
#    set_speed(spd)
#    motor0(forward0)
#    motor1(forward1)

#def rew(spd = 50):
#    set_speed(spd)
#    motor0(backward0)
#    motor1(backward1)

# steering
def center():
    turn(0)

def left():
    turn(30)  # CH0

def right():
    turn(-30)

def turn(angle):
    angle = Map(angle, 0, 255, leftPWM, rightPWM)
    pwm.write(0, 0, angle)

# exit
def turn_off():
    stop()
    center()

def calibrate(x):
    pwm.write(0, 0, 450+x)

def test():
   i=0
   while i<2:
       i += 1
       ffw(-50)
       time.sleep(3)
       ffw(50)
       time.sleep(3)
       ffw(100)
       turn(45)
       rew(50)
       time.sleep(3)
       turn(0)
       time.sleep(3)
       ffw(100)
       turn(-45)
       time.sleep(3)
       turn(0)
       time.sleep(3)


if __name__ == '__main__':
   setup()
   test()
   stop()
