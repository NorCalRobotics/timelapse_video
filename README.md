# Configuration:
Edit the file [config.json](config.json) to set up the time-lapse video capture process.
## smc_cam_hostname setting
Hostname of the
[SMC WIPCFN-G "Night vision IP Camera"](https://data2.manualslib.com/pdf2/37/3667/366667-smc_networks/wipcfng.pdf?c6851c21280a3337f495b88814bd2e3e&take=binary)
camera to connect to.
This can be an FQDN or an IP address.
## seconds_per_frame setting
Seconds of real time per frame in output video
Example value: 30
## fps setting
Frames per second in the output video.
Example value: 30.0
Example value: 40.0
Example value: 60.0
## frame_size setting
Photo and video resolution.
Required value: [616, 480] (SMC Camera's snapshot resolution)
## fourcc
4-CC code for the video, e.g. "mp4v",
## date_time_fmt
Format of the date/time when the script is started, to be used in the video output filename. 
Example value: "%Y%m%d_%H%M%S",
## mp4_filename_fmt
Format of the video output filename that will be set with the date/time when the script is started where "%s" in the
format string.
Example value: "C:\\Users\\Public\\Videos\\output_%s.mp4",
## img_cap_dir setting:
Set this value to the pathname of the local directory where the SMC camera is configured to store snapshot images.
This is where the collection of photos will be stored by the SMC camera's web interface.
Example value: "C:\\Users\\Public\\Pictures"
## delete_jpegs setting
If set to true, the snapshots will be deleted as they're processed, to save disk space.
The downside of this is that any errors during the process will result in lost data -- the video-making process can't be
re-tried later using [jpegs_to_timelapse_video.py](jpegs_to_timelapse_video.py) after the error.
Example value: true
Example value: false

# Live video capture mode (timelapse_video.py)
## Usage:
To execute the process, run [timelapse_video.py](timelapse_video.py) with your locally installed python3 interpreter as
per normal python procedures.

# Pre-existing sequence of still images in a directory mode (jpegs_to_timelapse_video.py)
## Configuration:
Edit [jpegs_to_timelapse_video.py](jpegs_to_timelapse_video.py) and set the variable `mp4_filename` to the name of the
video file to be re-generated from a previous run's snapshot files.
There will need to be a corresponding *_jpeg_list.txt file containing the filenames of the snapshot files that will make
up the frames of the video.
## Usage:
To execute the process, run [jpegs_to_timelapse_video.py](jpegs_to_timelapse_video.py) with your locally installed
python3 interpreter as per normal python procedures.

# Dependencies:
This project requires the modules [pyopencv](https://pypi.org/project/pyopencv/)
and [selenium](https://pypi.org/project/selenium).
You can install them using [pip](https://pypi.org/project/pip/):
run `pip install selenium pyopencv` as per normal [python](https://www.python.org/) procedures.
pyopencv requires a local [OpenCV](https://opencv.org/) installation; please see its documentation for help with that.

# Browser setup:
This obsolete SMC Camera only worked in Internet Exploder.
It uses an ActiveX (OCX) control embedded in its web interface.
Internet Explorer is obsolete and defunct now.
MS Edge has an Internet Explorer mode, that still works with the SMC Camera's ActiveX control.
The site must be in the list of sites that open in
[Edge's Internet Explorer mode](https://mcmw.abilitynet.org.uk/how-to-use-internet-explorer-mode-in-the-microsoft-edge-browser-for-windows-11).
The site must also be in the list of
[trusted sites](https://www.ias.edu/itg/content/how-add-trusted-sites-internet-explorer),
in order to save snapshots to your PC.
(You'll have to uncheck the checkbox that would not allow http sites to be trusted.)
Finally, make sure to configure the SMC web interface to set the directory for snapshots to be saved in,
to the same directory that is given in [config.json](config.json).
