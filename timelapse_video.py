import os
import time
import cv2
import json
from datetime import datetime
from signal import signal, SIGINT
from auto_fix_image_levels import adjust_image_colors
from smc_cam_snapshots import SMCIface, set_img_cap_dir

# settings
settings = json.load(open('config.json', 'r'))
smc_cam_hostname = settings['smc_cam_hostname']
seconds_per_frame = settings['seconds_per_frame']
fps = settings['fps']
frame_size = tuple(settings['frame_size'])
fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
date_time = datetime.now().strftime(settings['date_time_fmt'])
mp4_filename = settings['mp4_filename_fmt'] % date_time
jpeg_list_filename = os.path.splitext(mp4_filename)[0] + "_jpeg_list.txt"
if "img_cap_dir" in settings:
    set_img_cap_dir(settings["img_cap_dir"])

# Open the timelapse video output
mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, frame_size)

# Open the SMI Camera interface
smc_cam_interface = SMCIface(smc_cam_hostname)
if "delete_jpegs" in settings:
    smc_cam_interface.delete_jpegs = settings["delete_jpegs"]
time.sleep(10)

# Set up for the script to gracefully exit on SIGINT
ctrl_c_pressed = False


def ctrl_c_handler():
    global ctrl_c_pressed
    ctrl_c_pressed = True


signal(SIGINT, ctrl_c_handler)
smc_cam_interface.set_browser_closed_callback(ctrl_c_handler)
jpeg_list_file = open(jpeg_list_filename, 'w')


def on_image_capture(jpg_filename):
    print("Frame captured: " + os.path.basename(jpg_filename))
    jpeg_list_file.write(jpg_filename + "\n")


smc_cam_interface.set_snapshot_log_callback(on_image_capture)

# Loop until SIGINT, Ctrl-C, or Escape
while not ctrl_c_pressed:
    try:
        img = smc_cam_interface.get_snapshot_img()
        if img is None:
            continue

        # Adjust the image's levels
        img = adjust_image_colors(img)

        mp4_out.write(img)
        time.sleep(seconds_per_frame)
    except KeyboardInterrupt:
        ctrl_c_pressed = True

jpeg_list_file.close()

# Close the timelapse video output
print("Releasing MP4 Video Writer")
mp4_out.release()
print("Timelapse DONE")
