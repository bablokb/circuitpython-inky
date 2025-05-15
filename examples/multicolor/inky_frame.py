# -------------------------------------------------------------------------
# Inky-Frame base class
#
# Author: Bernhard Bablok
# License: MIT
#
# Website: https://github.com/bablokb/circuitpython-inky
# -------------------------------------------------------------------------

import board
import keypad

from inky_base import InkyBase

CS_PIN_SD = board.SD_CS
SR_CLOCK  = board.SWITCH_CLK
SR_LATCH  = board.SWITCH_LATCH
SR_DATA   = board.SWITCH_OUT

class InkyFrame_57(InkyBase):

  # --- constructor   -----------------------------------------------------

  def __init__(self, border_color=None,  # unused
               dither=False):
    """ constructor """

    self._LEDs = [board.LED_A, board.LED_B, board.LED_C,
                  board.LED_D, board.LED_E,
                  board.LED_ACT, board.LED_CONN, board.PICO_LED
                  ]
    super().__init__(self._LEDs,
                     [0xFFFFFF, 0x000000, 0x0000FF, 0x00FF00
                      0xFF0000, 0xFFFF00, 0xFFA500],
                     dither=dither
                    )

    self.display    = board.DISPLAY
    self._spi       = board.SPI()
    self._cs_pin_sd = CS_PIN_SD
    self._title     = "Inky-Frame 5.7"

  # --- return keypad for buttons and corresponding LEDs   ------------------

  def keypad(self):
    """ create and return keypad for buttons """

    # shift-register keys map in reverse order
    # "keys" 0-2 are busy, external trigger, rtc-alarm and unused here
    return (keypad.ShiftRegisterKeys(clock = SR_CLOCK,
                                     data  = SR_DATA,
                                     latch = SR_LATCH,
                                     key_count = 8,
                                     value_to_latch = True,
                                     value_when_pressed = True),
            list(range(7,-1,-1))
            )
