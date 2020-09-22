#!/bin/sh

ffmpeg -loglevel error -i $RTSP_URL -c copy -f segment -segment_time $BUFFER_INTERVAL -strftime 1 "$CACHE_DIR/%Y-%m-%dT%H-%M-%SZ.mp4"
