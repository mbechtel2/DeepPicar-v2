# init
def init(default_speed=50):
    set_speed(default_speed)

# throttle
MAX_SPEED = 100
cur_speed = MAX_SPEED

def set_speed(speed):
    global cur_speed
    speed = int(MAX_SPEED * speed / 100)
    cur_speed = min(MAX_SPEED, speed)

def get_speed():
    return int(cur_speed * 100 / MAX_SPEED)

def get_angle():
    return 0

def stop():
    return 
        
def ffw():
    return 

def rew():
    return 

# steering
def center():
    return get_angle()
def left():
    return get_angle()
def right():
    return get_angle()

# exit    
def turn_off():
    stop()
    center()
