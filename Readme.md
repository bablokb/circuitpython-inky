CircuitPython Drivers for various Pimoroni Inky-Displays
========================================================

In this repo you will find the module `inky` that has a number of
CircuitPython driver classes for Pimoroni Inky-Displays:

  - `inky/what.py`: two and three color e-Inks, 400x300
  - `inky/spectra6.py`: six color e-Inks (Spectra6)

The spectra6-driver currently only supports the 7.3-variant.
The driver probably also works withe the Spectra6-display from
Waveshare. Feedback on this assumption is welcome.


Examples
========

Various examples and test programs are in the `examples/` directory.

Prereqs for the examples:

  - adafruit_bitmap_font
  - adafruit_bus_device
  - adafruit_display_shapes
  - adafruit_display_text
  - adafruit_spd1656.mpy (for first generation Inky-Impression 4/5.7)


Dithering
=========

With only six or seven available colors, you need to dither normal
images to prevent a very blocky look.

The following steps are necessary:

  - resize the image to the target size
  - dither the image to the target color-palette
  - export the image in BMP-format

GUI tools like Gimp or Photoshop support the necessary operations, but
using the ImageMagick tools is much simpler. The `scripts`-directory
contains a number of scripts that help to automate the necessary
steps:

  - `colormap.sh`: create colormaps
  - `dither.sh`: create a dithered and resized BMP-version of an input image
  - `remap.sh`:  create a resized BMP-version of an input image without dithering
  - `color_patches.sh`: create a test-image with 216 colors of the given size

The first script is included for documentation only, since the
`scripts`-directory already includes two color-maps (files
`color6map.png` and `color7map.png`).  Note that these color maps are
only 1x6 and 1x7 pixels small and are used by the dither and remap scripts.

The test-image created with `color_patches.sh` has 216 colors and must
also be dithered or remapped before loading it to an Inky.

For background information regarding dithering, see
<https://usage.imagemagick.org/quantize/>.
