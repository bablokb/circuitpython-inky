# -------------------------------------------------------------------------
# CircuitPython driver for Pimoroni's Spectra-6 7.3" e-ink display.
#
# Author: Bernhard Bablok
# License: MIT
#
# This is a port of the inky_e673-driver from: https://github.com/pimoroni/inky
# The original MIT-License is Copyright (c) 2018 Pimoroni Ltd.
#
# Website: https://github.com/bablokb/circuitpython-inky
# -------------------------------------------------------------------------

import epaperdisplay
import fourwire

# pins used by the Inky-Impression (Pi names)
# RST: GPIO27
# BUSY: GPIO17
# DC: GPIO22

# TX: GPIO10
# CLK: GPIO11
# CS: GPIO8 (CS0)

# format: command length|delay args [delay]
_START_SEQUENCE = (
  b"\xAA\x06\x49\x55\x20\x08\x09\x18"    # ??
  b"\x01\x01\x3F"                        # PWR
  b"\x00\x02\x5F\x69"                    # PSR
  b"\x05\x04\x40\x1F\x1F\x2C"            # BTST1
  b"\x08\x04\x6F\x1F\x1F\x22"            # BTST3
  b"\x06\x04\x6F\x1F\x17\x17"            # BTST2
  b"\x03\x04\x00\x54\x00\x44"            # POFS
  b"\x60\x02\x02\x00"                    # TCON
  b"\x30\x01\x08"                        # PLL
  b"\x50\x01\x3F"                        # CDI
  b"\x61\x04\x03\x20\x01\xE0"            # TRES
  b"\xE3\x01\x2F"                        # PWS
  b"\x82\x01\x01"                        # VDCS
  b"\x04\80\xFE"                         # PON + plus delay of 0.254s
)

_STOP_SEQUENCE = (
  b"\x02\x81\x00\xFE"                    # POF + plus delay of 0.254s
)

_REFRESH_SEQUENCE = (
  b"\x06\x04\x6F\x1F\x17\x49"            # BTST2 (second setting)
  b"\x12\x01\x00"                        # DRF
)

class Inky_673(epaperdisplay.EPaperDisplay):
  """ Inky Impression Spectra-6 7.3in driver """

  def __init__(self, bus: fourwire.FourWire,
               border_color='white', **kwargs) -> None:

    super().__init__(
      bus,
      _START_SEQUENCE,
      _STOP_SEQUENCE,
      **kwargs,
      width=800,
      height=480,
      ram_width=800,
      ram_height=480,
      rotation=0,
      busy_state=False,
      write_black_ram_command=0x10,                  # DTM1
      refresh_display_command=_REFRESH_SEQUENCE,
      spectra6=True,
      seconds_per_frame=24,
      refresh_time=24.0,
    )
