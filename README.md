# Live video capture mode (timelapse_video.py)
## Configuration:
Edit the file [config.json](config.json) to set up the time-lapse video capture process.
#### seconds_per_frame setting
Seconds of real time per frame in output video
Example value: 30
#### fps setting
Frames per second in the output video.
Example value: 30.0
Example value: 40.0
Example value: 60.0
#### frame_size setting
Photo and video resolution.
Example value: [1280, 720] (720p video resolution)
#### fourcc
4-CC code for the video, e.g. "mp4v",
#### date_time_fmt
Format of the date/time when the script is started, to be used in the video output filename. 
Example value: "%Y%m%d_%H%M%S",
#### mp4_filename_fmt
Format of the video output filename that will be set with the date/time when the script is started where "%s" in the
format string.
Example value: "C:\\Users\\Public\\Videos\\output_%s.mp4",
#### vidcap_camera_index
Video source number on the PC to use.
Example value: 0
#### CAP_PROP_CHANNEL (optional)
If this is specified, then CAP_PROP_CHANNEL is set to the given value.
Example value: 40.1

## Usage:
To execute the process, run [timelapse_video.py](timelapse_video.py) with your locally installed python3 interpreter
as per normal python procedures.

# Stop-motion mode (stop_motion_capture.py)
## Configuration:
Same configuration as live video capture mode (timelapse_video.py), except that the seconds_per_frame setting
is ignored.

## Usage:
To execute the process, run [stop_motion_capture.py](stop_motion_capture) with your locally installed python3 interpreter
as per normal python procedures.

# Pre-existing sequence of still images in a directory mode (jpegs_to_timelapse_video.py)
## Configuration:
### Specify your photo collections:
Edit the file [img_sequence_config.json](img_sequence_config.json) to set the photo gallery directory that will
be processed.
#### fps setting
Frames per second in the output video.
Example value: 30.0
Example value: 40.0
Example value: 60.0
#### frame_size setting
Photo and video resolution.
Example value: [1920, 1080] (1080p video resolution)
#### fourcc
4-CC code for the video, e.g. "mp4v",
#### mp4_filename
Video output filename.
#### img_cap_dir setting:
Set this value to the pathname of the local directory where the collection of photos is stored.
#### img_glob_pattern
Set this value to specify the photos in the specified directory that will be selected.
Example value: "*.jpg" (All jpg files)

## Usage:
To execute the process, run [jpegs_to_timelapse_video.py](jpegs_to_timelapse_video.py) with your locally installed
python3 interpreter as per normal python procedures.

# Dependencies:
This project requires the module [pyopencv](https://pypi.org/project/pyopencv/).
You can install it using [pip](https://pypi.org/project/pip/):
run `pip install pyopencv` as per normal [python](https://www.python.org/) procedures.
pyopencv requires a local [OpenCV](https://opencv.org/) installation; please see its documentation for help with that.
