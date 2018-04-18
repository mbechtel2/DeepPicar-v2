import cv2
import local_common as cm
import os
import sys
import params

vid_path = "out-video.avi"
csv_path = "out-key.csv"

font = cv2.FONT_HERSHEY_SIMPLEX

if len(sys.argv) == 3:
    vid_path = sys.argv[1]
    csv_path = sys.argv[2]
elif len(sys.argv) == 2:
    epoch_id = int(sys.argv[1])
    vid_path = params.data_dir + '/out-video-{}.avi'.format(epoch_id)
    csv_path = params.data_dir + '/out-key-{}.csv'.format(epoch_id)

print params.data_dir, vid_path
assert os.path.isfile(vid_path)
assert os.path.isfile(csv_path)

frame_count = cm.frame_count(vid_path)
cap = cv2.VideoCapture(vid_path)
imgs = []
rows = cm.fetch_csv_data(csv_path)
print ("%d %d" % (frame_count, len(rows)))
assert frame_count == len(rows)
ts_init = rows[0]['ts_micro']
for i in range(frame_count):
    ret, img = cap.read()
    text = '{:.3f} {:3d} {:.3f}'.format(float((rows[i]['ts_micro']-ts_init))/1000.0,
                                  rows[i]['frame'], rows[i]['wheel'])
    cv2.putText(img, text, (5,50), font, 1.0, (255,255,255))
    imgs.append(img)

frame_id = 0
while True:
    cv2.imshow('frame', imgs[frame_id])
    ch = cv2.waitKey(0) # wait 
    if ch == ord('q'):
        break
    elif ch == ord('l'):
        frame_id = min(frame_id + 1, frame_count -1 )
    elif ch == ord('j'):
        frame_id = max(frame_id - 1, 0)
        
