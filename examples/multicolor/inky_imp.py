# -------------------------------------------------------------------------
# Inky-Impression base class and device specific classes.
#
# Author: Bernhard Bablok
# License: MIT
#
# Website: https://github.com/bablokb/circuitpython-inky
# -------------------------------------------------------------------------

import board
import busio
import displayio
import fourwire
import keypad

from inky_base import InkyBase

SCK_PIN   = board.SCLK
MOSI_PIN  = board.MOSI
MISO_PIN  = board.MISO
BUSY_PIN  = board.GPIO17
DC_PIN    = board.GPIO22
RST_PIN   = board.GPIO27
CS_PIN_D  = board.CE0
CS_PIN_SD = board.SD_CS
BTN_PINS  = [board.GPIO5, board.GPIO6, board.GPIO16, board.GPIO24]

# --- Inky-Impression base class   ----------------------------------------

class InkyImpression(InkyBase):

  # --- constructor   -----------------------------------------------------

  def __init__(self,driver,colors=None,dither=False,busy_pin=BUSY_PIN,**kwargs):
    """ constructor """

    if colors is None:
      colors = [0xFFFFFF, 0x000000, 0x0000FF, 0x00FF00,
                0xFF0000, 0xFFFF00, 0xFFA500]
    print(f"{colors=}")
    super().__init__([board.LED],colors,dither=dither)
    self._spi = busio.SPI(SCK_PIN,
                          MOSI=MOSI_PIN,MISO=MISO_PIN)

    self.display = self._display(driver,busy_pin,**kwargs)
    self._cs_pin_sd = CS_PIN_SD

  # --- free resources   ---------------------------------------------------

  def deinit(self):
    """ free resources """

    #if self._spi:
    #  self._spi.deinit()

  # --- create display   ----------------------------------------------------

  def _display(self,driver,busy_pin,**kwargs):
    """ create display """

    displayio.release_displays()
    display_bus = fourwire.FourWire(self._spi,
                                    command=DC_PIN,
                                    chip_select=CS_PIN_D,
                                    reset=RST_PIN, baudrate=24_000_000
                                    )
    return driver(display_bus,busy_pin=busy_pin,**kwargs)

  # --- return keypad for buttons and corresponding LEDs   ------------------

  def keypad(self):
    """ create and return keypad for buttons """

    # the Inky-Impression only has a single LED, so map all keys to index 0
    return (keypad.Keys(BTN_PINS,
                       value_when_pressed=keys[0],pull=True,
                       interval=0.1,max_events=4),
            [0]*len(BTN_PINS)
            )

# --- Product specific subclasses   -----------------------------------------

class InkyImpression4(InkyImpression):
  def __init__(self,dither=False):
    import adafruit_spd1656
    super().__init__(adafruit_spd1656.SPD1656,dither=dither,busy_pin=None,
                     width=640,height=400,
                     refresh_time=28,seconds_per_frame=40)
    self._title     = "Inky-Impression 4"

class InkyImpression57(InkyImpression):
  def __init__(self):
    import adafruit_spd1656
    super().__init__(adafruit_spd1656.SPD1656,dither=dither,
                     width=600,height=448,
                     refresh_time=28,seconds_per_frame=40)
    self._title     = "Inky-Impression 5.7"

class InkyImpression673(InkyImpression):
  def __init__(self,dither=False):
    from inky import spectra6
    super().__init__(spectra6.Inky_673,dither=dither,
                     colors = [0x000000, 0xFFFFFF, 0xFF0000,
                               0x00FF00, 0x0000FF, 0xFFFF00,
                               ])
    self._title     = "Inky-Impression(2025) 7.3"
