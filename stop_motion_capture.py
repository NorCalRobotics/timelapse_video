import cv2
import json
from datetime import datetime
from signal import signal, SIGINT
from auto_fix_image_levels import adjust_image_colors
from timelapse_video import ctrl_c_pressed, ctrl_c_handler, get_video_capture


def capture_stop_motion_video(** settings):
    global ctrl_c_pressed

    ctrl_c_pressed = False

    try:
        fps = settings['fps']
        frame_size = tuple(settings.get('frame_size', []))
        fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
        vidcap_camera_index = settings.get("vidcap_camera_index", 0)
        mp4_filename = settings['mp4_filename']
    except KeyError as ke:
        raise TypeError(ke.args[0] + ' is a required named argument')

    # Start capturing video from Camera
    vidcap, vidcap_w, vidcap_h = get_video_capture(vidcap_camera_index, frame_size, settings)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Open the stop-motion video output
    mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, (vidcap_w, vidcap_h))

    signal(SIGINT, ctrl_c_handler)

    # Loop until SIGINT, Ctrl-C, or Escape
    instr1 = "Press ESC to exit."
    instr2 = "Press F to capture a frame."
    frame_count = 0
    k = None
    frame_count_msg = "%d frames captured" % frame_count
    while not ctrl_c_pressed:
        try:
            # Take each frame
            _, img = vidcap.read()

            if k is not None and k in [ord('f'), ord('F')]:
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
            cv2.putText(img, instr2, (20, 116), font, 0.4, (255, 255, 255), 1)
            cv2.putText(img, frame_count_msg, (20, 132), font, 0.4, (255, 255, 255), 1)

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


def main():
    # settings
    settings = json.load(open('config.json', 'r'))

    try:
        date_time = datetime.now().strftime(settings['date_time_fmt'])
        mp4_filename = settings['mp4_filename_fmt'] % date_time
    except KeyError as ke:
        raise TypeError(ke.args[0] + ' is a required config setting')

    settings['mp4_filename'] = mp4_filename

    capture_stop_motion_video(** settings)


if __name__ == "__main__":
    main()

