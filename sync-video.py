import cv2
import local_common as cm
import os
import sys

font = cv2.FONT_HERSHEY_SIMPLEX

if len(sys.argv) == 3:
    epoch_id = int(sys.argv[1])
    skip_count = int(sys.argv[2])
    vid_path = 'epochs/out-video-{}.avi'.format(epoch_id)
    csv_path = 'epochs/out-key-{}.csv'.format(epoch_id)
    conv_vid_path = 'epochs-conv/out-video-{}.avi'.format(epoch_id)
    conv_csv_path = 'epochs-conv/out-key-{}.csv'.format(epoch_id)
else:
    sys.exit(1)

print ("epoch_id: {}, skip_count: {}".format(epoch_id, skip_count))

assert os.path.isfile(vid_path)
assert os.path.isfile(csv_path)

frame_count = cm.frame_count(vid_path)
cap = cv2.VideoCapture(vid_path)
cam_width = int(cap.get(3))
cam_height = int(cap.get(4))
cam_fps = int(cap.get(5))

print ("w: {}, h:{}, fps: {}".format(cam_width, cam_height, cam_fps))

rows = cm.fetch_csv_data(csv_path)
assert frame_count == len(rows)

# data files
# fourcc = cv2.cv.CV_FOURCC(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vidfile = cv2.VideoWriter(conv_vid_path, fourcc,
                          cam_fps, (cam_width, cam_height))
keyfile = open(conv_csv_path, 'w+')
keyfile.write("ts_micro,frame,wheel\n")

# skip video frames
for i in range(skip_count):
    ret, img = cap.read()

# record adjusted data
for i in range(frame_count-skip_count):    
    # write input (angle)
    text = "{},{},{}\n".format(rows[i]['ts_micro'],
                               rows[i]['frame'], rows[i]['wheel'])
    keyfile.write(text)
    ret, img = cap.read()
    vidfile.write(img)

print("Close files.")
cap.release()
keyfile.close()
vidfile.release()

print("Validate converted data count")
frame_count = cm.frame_count(conv_vid_path)
rows = cm.fetch_csv_data(conv_csv_path)
assert frame_count == len(rows)
