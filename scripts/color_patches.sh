#!/bin/bash

# create 256c color-patches

if [ -z "$2" ]; then
  echo "usage: $0 size outfile" >&2
  exit 3
fi

size="$1"
outfile="$2"

convert netscape: -sample "$size!" -colors 256 "$outfile"
