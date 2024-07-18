#!/usr/bin/env bash

INPUT_MP4="${1}"
shift
OUTPUT_MP4=$(echo "${INPUT_MP4}" | sed 's/^\(.*\)\(\.[^.]*\)$/\1_tcd\2/')

ffmpeg -i "${INPUT_MP4}" \
  -c:v libx264 -crf 21 -preset faster -pix_fmt yuv420p -maxrate 5000K \
  -vf 'scale=if(gte(iw\,ih)\,min(1920\,iw)\,-2):if(lt(iw\,ih)\,min(1920\,ih)\,-2)' \
  -bufsize 5000K -movflags +faststart -c:a aac -b:a 160k \
  "${OUTPUT_MP4}" "$@"