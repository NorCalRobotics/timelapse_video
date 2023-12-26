import os
import cv2
import json
from auto_fix_image_levels import adjust_image_colors

# settings
settings = json.load(open('config.json', 'r'))
fps = settings['fps']
frame_size = tuple(settings['frame_size'])
fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
img_cap_dir = settings["img_cap_dir"]
vid_out_dir = os.path.dirname(settings['mp4_filename_fmt'])

mp4_filename = vid_out_dir + "/output_20231225.mp4"
jpeg_list_filename = os.path.splitext(mp4_filename)[0] + "_jpeg_list.txt"

# Open the timelapse video output
mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, frame_size)

with open(jpeg_list_filename, 'r') as jpeg_list_file:
    for line in jpeg_list_file:
        jpeg_filename = line.rstrip()
        print("frame " + jpeg_filename)
        img = cv2.imread(jpeg_filename)
        if img is None:
            print("Warning: skipping null frame " + jpeg_filename)
            continue
        img = adjust_image_colors(img)
        mp4_out.write(img)

print("Releasing MP4 Video Writer")
mp4_out.release()
print("Timelapse DONE")
