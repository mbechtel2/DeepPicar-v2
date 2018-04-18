import os
import time
import atexit
import termios, fcntl, sys, os
import select

def init():
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    return (flags_save, attrs_save)

def stop(state):
    fd = sys.stdin.fileno()
    # restore old state
    termios.tcsetattr(fd, termios.TCSAFLUSH, state[1])
    fcntl.fcntl(fd, fcntl.F_SETFL, state[0])
    
def read_single_keypress():
    state = init()    
    r, w, e = select.select([sys.stdin], [], [], 0.000)
    input = ' '
    for s in r:
        if s == sys.stdin:
            input = sys.stdin.read(1)
            break
    stop(state)
    return input

if __name__ == "__main__":

    while True:
        key = read_single_keypress()
        if key == "q":
            break
        elif key != ' ':
            print ("%s pressed\r" % key)
        

    
