import os
import cv2
import json
import glob
from auto_fix_image_levels import adjust_image_colors


# settings
settings = json.load(open('img_sequence_config.json', 'r'))
fps = settings['fps']
frame_size = tuple(settings['frame_size'])
fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
img_cap_dir = settings["img_cap_dir"]
mp4_filename = settings['mp4_filename']
img_glob_pattern = settings["img_glob_pattern"]

# Open the timelapse video output
mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, frame_size)

for jpeg_filename in glob.glob(os.path.join(img_cap_dir, img_glob_pattern)):
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
