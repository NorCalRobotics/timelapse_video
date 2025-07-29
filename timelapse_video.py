#!/usr/bin/env python3
import time
import cv2
import json
from datetime import datetime
from signal import signal, SIGINT
from auto_fix_image_levels import adjust_image_colors
try:
    import streamlink
except ModuleNotFoundError:
    streamlink = None

# Set up for the script to gracefully exit on SIGINT
ctrl_c_pressed = False


def ctrl_c_handler():
    global ctrl_c_pressed

    ctrl_c_pressed = True


def is_streaming_site(url):
    if streamlink is None:
        return False, None

    session = streamlink.Streamlink()
    print('streamlink version ' + streamlink.__version__)
    for plugin_name, matcher_list in session.plugins.iter_matchers():
        for matcher in matcher_list:
            if matcher.pattern.match(url):
                return True, plugin_name

    return False, None


def get_video_capture(vidcap_camera_index, frame_size, settings):
    # Start capturing video from Camera
    yt_mode, plugin_name = is_streaming_site(vidcap_camera_index)
    if yt_mode:
        print(plugin_name + " mode:")
        if "youtube_stream_key" in settings:
            youtube_stream_key = settings["youtube_stream_key"]
            print("From config: youtube_stream_key = '%s'" % youtube_stream_key)
        else:
            youtube_stream_key = 'best'
            print("config doesn't specify youtube_stream_key, using 'best'")
        streams = streamlink.streams(vidcap_camera_index)
        print(plugin_name + " vid url: " + vidcap_camera_index)
        print(plugin_name + " vid streams: " + ", ".join(streams.keys()))
        url = streams[youtube_stream_key].url
        print("%s Stream url: %s" % (youtube_stream_key, url))
        vidcap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
        vidcap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        vidcap.set(cv2.CAP_PROP_FPS, 20)
    else:
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

    fourcc = vidcap.get(cv2.CAP_PROP_FOURCC)
    codec = "".join([chr((int(fourcc) >> 8 * i) & 0xFF) for i in range(4)])
    print("Codec: " + codec)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print("FPS: " + str(fps))

    backend_name = vidcap.getBackendName()
    print("Backend: " + backend_name)

    return vidcap, vidcap_w, vidcap_h


def capture_timelapse_video(** settings):
    global ctrl_c_pressed

    ctrl_c_pressed = False

    try:
        seconds_per_frame = settings['seconds_per_frame']
        fps = settings['fps']
        frame_size = tuple(settings.get('frame_size', []))
        fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
        vidcap_camera_index = settings.get("vidcap_camera_index", 0)
        mp4_filename = settings['mp4_filename']
    except KeyError as ke:
        raise TypeError(ke.args[0] + ' is a required named argument')

    # Start capturing video from Camera
    vidcap,vidcap_w, vidcap_h = get_video_capture(vidcap_camera_index, frame_size, settings)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Open the timelapse video output
    mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, (vidcap_w, vidcap_h))

    signal(SIGINT, ctrl_c_handler)

    # Loop until SIGINT, Ctrl-C, or Escape
    instr1 = "Press ESC to exit."
    last_time = time.monotonic()  # None
    frame_count = 0
    established = False
    frame_count_msg = "%d frames captured" % frame_count
    while not ctrl_c_pressed:
        try:
            # Take each frame
            _, img = vidcap.read()
            if img is None:
                if established:
                    break
                else:
                    continue

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
                try:
                    cv2.imshow('Color-corrected frame', selected_frame)
                except cv2.error:
                    if established:
                        break

            cv2.putText(img, instr1, (20, 100), font, 0.4, (255, 255, 255), 1)
            cv2.putText(img, frame_count_msg, (20, 116), font, 0.4, (255, 255, 255), 1)
            if last_time is not None:
                seconds_until_next_frame = seconds_per_frame - (current_time - last_time)
                message = "%f seconds until next frame" % seconds_until_next_frame
                cv2.putText(img, message, (20, 132), font, 0.4, (255, 255, 255), 1)

            # Display the frame to the user, creating a live preview window
            try:
                cv2.imshow('Live preview', img)
                established = True
            except cv2.error as cv_e:
                if established:
                    break
                else:
                    print('Warning: ' + cv_e.msg)

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


def main():
    # settings
    settings = json.load(open('config.json', 'r'))

    try:
        date_time = datetime.now().strftime(settings['date_time_fmt'])
        mp4_filename = settings['mp4_filename_fmt'] % date_time
    except KeyError as ke:
        raise TypeError(ke.args[0] + ' is a required config setting')

    settings['mp4_filename'] = mp4_filename

    capture_timelapse_video(** settings)


if __name__ == "__main__":
    main()
