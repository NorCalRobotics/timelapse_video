import time
import cv2
import json
from datetime import datetime
from signal import signal, SIGINT
from auto_fix_image_levels import adjust_image_colors

# settings
settings = json.load(open('config.json', 'r'))
seconds_per_frame = settings['seconds_per_frame']
fps = settings['fps']
frame_size = tuple(settings.get('frame_size', []))
fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
date_time = datetime.now().strftime(settings['date_time_fmt'])
mp4_filename = settings['mp4_filename_fmt'] % date_time
vidcap_camera_index = settings["vidcap_camera_index"]

# Start capturing video from Camera
vidcap = cv2.VideoCapture(vidcap_camera_index)
if "CAP_PROP_CHANNEL" in settings:
    print("Setting video channel: %f" % settings["CAP_PROP_CHANNEL"])
    vidcap.set(cv2.CAP_PROP_CHANNEL, settings["CAP_PROP_CHANNEL"])
if len(frame_size) > 1:
    print("Setting video resolution: %dx%d" % frame_size)
    vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_size[0])
    vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_size[1])
vidcap_w = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
vidcap_h = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Video resolution: %dx%d" % (vidcap_w, vidcap_h))
font = cv2.FONT_HERSHEY_SIMPLEX

# Open the timelapse video output
mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, (vidcap_w, vidcap_h))

# Set up for the script to gracefully exit on SIGINT
ctrl_c_pressed = False


def ctrl_c_handler():
    global ctrl_c_pressed
    ctrl_c_pressed = True


signal(SIGINT, ctrl_c_handler)

# Loop until SIGINT, Ctrl-C, or Escape
instr1 = "Press ESC to exit."
last_time = time.monotonic()  # None
frame_count = 0
frame_count_msg = "%d frames captured" % frame_count
while not ctrl_c_pressed:
    try:
        # Take each frame
        _, img = vidcap.read()

        current_time = time.monotonic()
        if last_time is None or (current_time - last_time) > seconds_per_frame:
            last_time = current_time

            # Adjust the image's levels
            # This helps with lighting changes over time
            selected_frame = adjust_image_colors(img)

            # Add this frame to the video
            mp4_out.write(selected_frame)

            frame_count += 1
            frame_count_msg = "%d frames captured" % frame_count

            # Display the adjusted frame to the user
            cv2.imshow('Color-corrected frame', selected_frame)

        cv2.putText(img, instr1, (20, 100), font, 0.4, (255, 255, 255), 1)
        cv2.putText(img, frame_count_msg, (20, 116), font, 0.4, (255, 255, 255), 1)
        if last_time is not None:
            seconds_until_next_frame = seconds_per_frame - (current_time - last_time)
            message = "%f seconds until next frame" % seconds_until_next_frame
            cv2.putText(img, message, (20, 132), font, 0.4, (255, 255, 255), 1)

        # Display the frame to the user, creating a live preview window
        cv2.imshow('Live preview', img)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            ctrl_c_pressed = True
    except KeyboardInterrupt:
        ctrl_c_pressed = True

cv2.destroyAllWindows()

# Close the timelapse video output
print("Releasing MP4 Video Writer")
mp4_out.release()
print("Timelapse DONE")
