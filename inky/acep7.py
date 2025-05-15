# -------------------------------------------------------------------------
# CircuitPython driver for Pimoroni's 7-color Inky-Impression 4"/5.7"
# displays. Note that this driver does not support the pre-2025 7.3" version.
#
# Author: Bernhard Bablok
# License: MIT
#
# This is a tweaked version of Adafruit's SPD1656-driver from
# https://github.com/adafruit/Adafruit_CircuitPython_SPD1656
# This version supports the additional kwarg 'border_color' (default: WHITE).
#
# The original MIT-License is
# Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
#
# Website: https://github.com/bablokb/circuitpython-inky
# -------------------------------------------------------------------------

import struct
import epaperdisplay

# valid border-colors
BLACK = 0
WHITE = 1
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6
CLEAN = 7

_START_SEQUENCE = (
  b"\x01\x04\x37\x00\x23\x23"  # power setting
  b"\x00\x02\xef\x08"  # panel setting (PSR)
  b"\x03\x01\x00"  # PFS
  b"\x06\x03\xc7\xc7\x1d"  # booster
  b"\x30\x01\x3c"  # PLL setting
  b"\x41\x01\x00"  # TSE
  b"\x50\x01\x37"  # vcom and data interval setting (border-color: 1==white)
  b"\x60\x01\x22"  # tcon setting
  b"\x61\x04\x02\x58\x01\xc0"  # tres
  b"\xe3\x01\xaa"  # PWS
  b"\x04\x80\xc8"  # power on and wait 10 ms
)

_STOP_SEQUENCE = b"\x02\x01\x00" b"\x07\x01\xA5"  # Power off then deep sleep

class ACEP7(epaperdisplay.EPaperDisplay):
  r"""acep7 aka SPD1656 display driver

  :param bus: The data bus the display is on
  :param \**kwargs:
    See below

  :Keyword Arguments:
    * *width* (``int``) --
      Display width
    * *height* (``int``) --
      Display height
    * *rotation* (``int``) --
      Display rotation
    """

  def __init__(self, bus, border_color=None, **kwargs):
    if border_color is None:
      border_color = WHITE
    else:
      border_color = int(border_color)
      if border_color < 0 or border_color > 7:
        raise ValueError("unsupported border-color")

    width = kwargs["width"]
    height = kwargs["height"]
    if "rotation" in kwargs and kwargs["rotation"] % 180 != 0:
      width, height = height, width

    start_sequence = bytearray(_START_SEQUENCE)

    if height <= 320:
      resa = 0
    else:
      resa = 1

    if width == 640:
      res0 = 0
    else:
      res0 = 1

    if height == 448:
      res1 = 1
    else:
      res1 = 0

    # Patch PSR's display resolution setting
    start_sequence[8] |= res1 << 7 | res0 << 6 | resa << 5

    # Patch tres
    struct.pack_into(">HH", start_sequence, 32, width, height)

    # Patch CDI
    start_sequence[26] = (border_color << 5) | 0x17

    # This assumes the chip is used for an ACeP display even though the
    # datasheet is documented as 4 grays and 4 reds.
    super().__init__(
      bus,
      start_sequence,
      _STOP_SEQUENCE,
      **kwargs,
      ram_width=640,
      ram_height=480,
      start_up_time=1,
      busy_state=False,
      write_black_ram_command=0x10,
      refresh_display_command=0x12,
      advanced_color_epaper=True
    )
