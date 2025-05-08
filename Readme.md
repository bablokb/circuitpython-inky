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
