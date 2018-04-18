import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

cap.set(3, 320) # width
cap.set(4, 240) # height
cap.set(5, 30)

while(True):
    ts = time.time()    
    # Capture frame-by-frame
    ret, frame = cap.read()
    dur = int((time.time() - ts) * 1000);
    
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print ("%.3f %d(ms)" % (ts, dur))    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
