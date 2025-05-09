#!/bin/bash

# create colormap (pass number of colors as argument)

# Note that colors are varbatim copies of the Pimoroni drivers.
# These colors are probably not an optimal choice

declare -a COLORS=( \
  "(0,0,0)" \
  "(255,255,255)" \
  "(0,255,0)" \
  "(0,0,255)" \
  "(255,0,0)" \
  "(255,255,0)" \
  "(255,140,0)" \
)

# no need to resize, just for debugging
#RESIZE="-resize 100x100"

colors="$1"
outfile="${2:-./color${colors}map.png}"

declare -a args=()
for c in "${COLORS[@]:0:$colors}"; do
  args+=("xc:rgb$c")
done

convert "${args[@]}" $RESIZE +append "$outfile"
