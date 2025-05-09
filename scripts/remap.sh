#!/bin/bash

# scale and remap an image: remap.sh infile colors size outfile

if [ -z "$1" ]; then
  echo "usage: $0 infile [colors [size [outfile]]]" >&2
  exit 3
fi

# set some defaults
colors="${2:-6}"
size="${3:-800x480}"
outfile="${4:-${1/.jpg/.bmp}}"

convert "$1" -colorspace RGB -resize "$size!" +dither \
              -remap "$(dirname $0)/color${colors}map.png" "$outfile"
