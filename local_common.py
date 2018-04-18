from __future__ import division

import datetime
import time
import numpy as np
from collections import OrderedDict, Counter
import re
import os
import csv
import cv2
import sys
import copy
import subprocess as sp
from numpy.fft import fft, ifft, fft2, ifft2, fftshift


host_options = 'hal, turing, lex-laptop'.split(', ')

postgres_int_type = 'int'
postgres_long_type = 'bigint'
postgres_double_type = 'float8'
postgres_string_type = 'text'
postgres_null_type = 'null'


def pretty_time_left(time_start, iterations_finished, total_iterations):   
    if iterations_finished == 0:
        time_left = 0
    else:
        time_end = time.time()
        diff_finished = time_end - time_start
        time_per_iteration = diff_finished / iterations_finished
        assert time_per_iteration >= 0
        
        iterations_left = total_iterations - iterations_finished
        assert iterations_left >= 0
        time_left = int(round(iterations_left * time_per_iteration))

    return pretty_dur(time_left)

   
def pretty_running_time(time_start):
    time_end = time.time()
    diff = int(round(time_end - time_start))

    return pretty_dur(diff)

def split_secs(ts_secs):
    dt = datetime.datetime.utcfromtimestamp(ts_secs)
    h, m, s, ms, us = split_datetime(dt)
    return h, m, s, ms, us

def split_datetime(dt):
    h, m, s, us = dt.hour, dt.minute, dt.second, dt.microsecond
    ms = int(round(us / 1000))
    us = us % 1000

    return h, m, s, ms, us


def pretty_dur(dur, fmt_type='full'):
    assert fmt_type in 'minimal, compressed, full'.split(', ')
    
    assert dur >= 0
    h, m, s, ms, us = split_secs(dur)

    if fmt_type == 'minimal':
        dur_str = '{:0>2}:{:0>2}:{:0>2}.{:0>3}'.format(h, m, s, ms)
    elif fmt_type == 'compressed':
        dur_str = '{:0>2}h {:0>2}m {:0>2}.{:0>3}s'.format(h, m, s, ms)
    else:
        dur_str = '{:0>2} hours {:0>2} mins {:0>2} secs {:0>3} msecs'.format(h, m, s, ms)

    return dur_str

def is_sequence(arg):
    return (not hasattr(arg, 'strip') and 
            hasattr(arg, '__getitem__') and
            hasattr(arg, '__iter__'))

def is_int(s):
    assert not is_sequence(s)

    try: 
        int(s)
        return True
    except ValueError:
        return False

def is_str(obj):
    return isinstance(obj, basestring)

def is_long(s):
    assert not is_sequence(s)

    try: 
        long(s)
        return True
    except ValueError:
        return False

def is_number(s):
    assert s is not None
    assert not is_sequence(s)

    if is_str(s) and (',' in s): # '1,000' is not a number since it has a comma and that could mean a lot of things
        return False

    try:
        float(s)
        return True
    except ValueError:
        return False

def get_postgres_type_from_variable(x):
    if x is None:
        return postgres_null_type
    elif is_str(x):
        return get_postgres_type_from_str(x)
    elif isinstance(x, int) or isinstance(x, long):
        return postgres_long_type
    elif isinstance(x, float) or isinstance(x, decimal.Decimal):
        return postgres_double_type
    else:
        print 'Incorrect type is {}'.format(type(x))
        assert False

def get_postgres_type_from_str(s):
    assert not is_sequence(s)
    if is_long(s):
        return postgres_long_type
    elif is_number(s):
        return postgres_double_type
    else:
        return postgres_string_type

def cast_str_to_type_force(s, type_to_force):
    if type_to_force == postgres_int_type:
        assert is_int(s)
        return int(s)
    elif type_to_force == postgres_long_type:
        assert is_long(s)
        return long(s)
    elif type_to_force == postgres_double_type:
        assert is_number(s)
        return float(s)
    elif type_to_force == postgres_string_type:
        return s
    else:
        assert False

def postgres_type_order(t):
    return {
        None : 0,
        postgres_null_type : 1,
        postgres_long_type : 2,
        postgres_double_type : 3,
        postgres_string_type : 4,
    }[t]

def postgres_common_type(t1, t2):
    if postgres_type_order(t1) < postgres_type_order(t2):
        return t2
    else:
        return t1

def determine_types_from_rows(rows, consider_only_a_sample=True):
    assert len(rows) > 0
    
    if consider_only_a_sample:
        sample_size = 100
    else:
        sample_size = len(rows)

    # if there are more than 10 rows then we sample 10 random rows
    if len(rows) <= sample_size:
        rows_sampled = rows
    else:
        rows_sampled = random.sample(rows, sample_size)

    assert len(rows_sampled) > 0
    types = [None] * len(rows_sampled[0])
    for row in rows_sampled:
        assert len(types) == len(row)
        
        if isinstance(row, OrderedDict):
            vals = row.values()
        elif isinstance(row, list):
            vals = row
        else:
            assert False

        for i, x in enumerate(vals):
            t_old = types[i]
            t_new = get_postgres_type_from_variable(x)
            
            types[i] = postgres_common_type(t_old, t_new)
    
    return types

def apply_types_to_row(types, row):
    assert len(types) == len(row)

    if isinstance(row, OrderedDict):
        keys = row.keys()
        vals = row.values()
    elif isinstance(row, list):
        vals = row
    else:
        assert False

    for i, x in enumerate(vals):
        vals[i] = cast_str_to_type_force(x, type_to_force=types[i])

    if isinstance(row, OrderedDict):
        return OrderedDict(zip(keys, vals))
    elif isinstance(row, list):
        return vals

def apply_types_to_rows(types, rows):
    results = []
    for row in rows:
        results.append(apply_types_to_row(types, row))
    return results

def fetch_csv_data(filepath, delimiter=',', consider_only_a_sample=False, univ_new_line=False,
                   include_only_these_fields=None, clean_up_field_names=False,
                   unique_index_fields=None):    
    assert os.path.isfile(filepath)
    data_raw = []

    open_flag = 'rb'
    open_flag += 'U' if univ_new_line else ''
    row_counter = 0

    with open(filepath, open_flag) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        fields = None
        
        for row in reader:
            row_counter += 1
            #if row_counter % 1000 == 0: print 'loaded {} rows'.format(row_counter)
            
            assert len(row) > 1
            if fields is None:
                fields = row
                if clean_up_field_names:
                    fields = [f.replace(' ', '_').lower() for f in fields]
                continue

            if len(fields) != len(row):
                print 'fields:', fields
                print 'row:', row
                                    
            assert len(fields) == len(row)

            # remove fields not in 'include_only_these_fields' if it's defined
            if include_only_these_fields is None:
                d = OrderedDict(zip(fields, row))
            else:
                assert set(include_only_these_fields).issubset(set(fields))
                d = OrderedDict()
                for i, f in enumerate(fields):
                    if f in include_only_these_fields:
                        d[f] = row[i]
            
            data_raw.append(d)

    types = determine_types_from_rows(data_raw, consider_only_a_sample)

    data = apply_types_to_rows(types, data_raw)

    if unique_index_fields is not None:
        data = add_unique_index_to_row_of_dicts(data, unique_index_fields)

    return data    


def overlay_image(l_img, s_img, x_offset, y_offset):
    assert y_offset + s_img.shape[0] <= l_img.shape[0]
    assert x_offset + s_img.shape[1] <= l_img.shape[1]

    l_img = l_img.copy()
    for c in range(0, 3):
        l_img[y_offset:y_offset+s_img.shape[0],
              x_offset:x_offset+s_img.shape[1], c] = (
                  s_img[:,:,c] * (s_img[:,:,3]/255.0) +
                  l_img[y_offset:y_offset+s_img.shape[0],
                        x_offset:x_offset+s_img.shape[1], c] *
                  (1.0 - s_img[:,:,3]/255.0))
    return l_img

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape)/2)[:2]
    rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[:2], flags=cv2.INTER_LINEAR)
    return result

def jn(dirpath, filename):
    return os.path.join(dirpath, filename)

def video_resolution_to_size(resolution, width_first=True):
    if resolution == '720p':
        video_size = (1280, 720)
    elif resolution == '1080p':
        video_size = (1920, 1080)
    elif resolution == '1440p':
        video_size = (2560, 1440)
    elif resolution == '4k':
        video_size = (3840, 2160)
    else: assert False

    if not width_first:
        video_size = (video_size[1], video_size[0])
    return video_size


def imread(img_path, mode=cv2.IMREAD_COLOR):
    assert os.path.isfile(img_path), 'Bad image path: {}'.format(img_path)
    return cv2.imread(img_path, mode)
    
    
def cv2_resize_by_height(img, height):
    ratio = height / img.shape[0]
    width = ratio * img.shape[1]
    height, width = int(round(height)), int(round(width))
    return cv2.resize(img, (width, height))

def frame_count(path, method='ffmpeg'):
    if method == 'ffmpeg':
        return ffmpeg_frame_count(path)
    elif method == 'opencv_instant':
        return cv2_frame_count(path)
    elif method == 'opencv_full':
        return cv2_frame_count_manual(path)
    elif method == 'opencv_ffprobe':
        return ffprobe_frame_count(path)
    else:
        assert False


def ffmpeg_frame_count(path):
    cmd = 'ffmpeg -i {} -vcodec copy -acodec copy -f null /dev/null 2>&1'.format(path)
    cmd_res = sp.check_output(cmd, shell=True)
    cmd_res = copy.deepcopy(cmd_res)

    fc = None

    lines = cmd_res.splitlines()
    lines = lines[::-1]

    for line in lines:
        line = line.strip()
        res = re.match(r'frame=\s*(\d+)\s*fps=', line)
        if res:
            fc = res.group(1)
            
            assert is_int(fc)
            fc = int(fc)
            break

    assert fc is not None

    return fc

def cv2_current_frame(cap):
    x = cap.get(cv2.CAP_PROP_POS_FRAMES)
    assert x.is_integer()
    return int(x)

def cv2_goto_frame(cap, frame_id):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    assert cv2_current_frame(cap) == frame_id

def without_ext(path): 
    return os.path.splitext(path)[0]

def ext(path, period=False):
    x = os.path.splitext(path)[1]
    x = x.replace('.', '')
    return x

def mkv_to_mp4(mkv_path, remove_mkv=False):
    assert os.path.isfile(mkv_path)
    assert ext(mkv_path) == 'mkv'
    mp4_path = without_ext(mkv_path) + '.mp4'
    
    if os.path.isfile(mp4_path):
        os.remove(mp4_path)
    
    cmd = 'ffmpeg -i {} -c:v copy -c:a libfdk_aac -b:a 128k {} >/dev/null 2>&1'.format(mkv_path, mp4_path)
    sp.call(cmd, shell=True)

    assert os.path.isfile(mp4_path) # make sure that the file got generated successfully

    if remove_mkv:
        assert os.path.isfile(mkv_path)
        os.remove(mkv_path)
    


