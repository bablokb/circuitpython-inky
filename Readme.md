CircuitPython Drivers for various Pimoroni Inky-Displays
========================================================

In this repo you will find the module `inky` that has a number of
CircuitPython driver classes for Pimoroni Inky-Displays:

  - `inky/what.py`: two and three color e-Inks, 400x300
  - `inky/acep7.py`: seven color e-Inks (Inky-Impression 4"/5.7")
  - `inky/spectra6.py`: six color e-Inks (Spectra6)

The acep7-driver does not support the 7.3"-variant.

The spectra6-driver currently only supports the 7.3-variant.
The driver probably also works with the Spectra6-display from
Waveshare. Feedback on this assumption is welcome.

Missing support for various Inkys is due to missing test devices. The
implementation of suitable drivers should be straightforward.

For the Inky-Frames 5.7" and 7.3" there are pre-built CircuitPython
versions available that have builtin support for the respective
displays, so no separate driver is necessary.


A note on `seconds_per_frame` and `refresh_time`
------------------------------------------------

The acep7/spectra6-driver define default values for `seconds_per_frame` and
`refresh_time`.

  - `refresh_time` is the time it takes from start of `display.refresh()` until
    the display has actually refreshed. `display.refresh()` will return before
    the refresh is finished, but will keep the `busy`-attribute `True`. As long
    as you provide a busy-pin, the `refresh_time` is ignored. Since the
    Inky-Impression has a busy-pin, the refresh-time is only used to document the
    expected update-time of the display.

  - `seconds_per_frame` is the time from start of (internal) display refresh
    until the refresh has finished. It should read as 'extra seconds per frame'
    in the context of e-ink displays. Idealy, `refresh_time-seconds_per_frame`
    is the raw internal display refresh-time. The reason to set this value so low
    is to allow a new refresh to start immediately after the busy-state is
    `False` again. This should only be necessary in the context of program
    development and tests.

There is no documentation on how often you can update the
display. Nevertheless, it should not be updated often. Once an hour is
probably already too often.


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
