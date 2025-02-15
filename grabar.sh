#!/bin/bash

[ -z "$1" ] && exit 1

sleep 2

arecord -d 3 -f cd -r 44100 -t wav "$1".wav

ffmpeg -i "$1".wav -af afftdn=nf=-50 "$1"-tmp.wav

mv "$1"-tmp.wav "$1".wav
