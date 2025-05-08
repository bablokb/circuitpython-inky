# -------------------------------------------------------------------------
# Testprogram for Pimoroni's wHat e-ink display.
#
# This program is an adaption of Adafruit's uc8151d_simpletest.py from
# https://github.com/adafruit/Adafruit_CircuitPython_UC8151D
#
# The display is for a Pi and to run it with something else, you need
# either additional wiring or an adapter (e.g. from
# https://github.com/bablokb/pcb-pico-pi-base)
#
# Author: Bernhard Bablok
# License: MIT
#
# Website: https://github.com/bablokb/circuitpython-inky
# -------------------------------------------------------------------------

# pylint: disable=no-member

import time
import board
import busio
import displayio
from inky.what import Inky_wHat

print("starting program")
time.sleep(5)

print("releasing displays")
displayio.release_displays()

# pinout for Pimoroni wHat (Pi-names)

SCK_PIN  = board.GPIO11
MOSI_PIN = board.GPIO10
CS_PIN   = board.CE0
RST_PIN  = board.GPIO27
DC_PIN   = board.GPIO22
BUSY_PIN = board.GPIO17

spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN)
display_bus = displayio.FourWire(
  spi, command=DC_PIN, chip_select=CS_PIN, reset=RST_PIN, baudrate=488000
)

print("creating display")
display = Inky_wHat(display_bus,busy_pin=BUSY_PIN,border_color='white',
                    black_bits_inverted=True)

print("creating root-group")
g = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
  pic = displayio.OnDiskBitmap(f)
  t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
  print("appending image")
  g.append(t)

  display.root_group = g
  print("starting refresh()")
  display.refresh()
  print("finished")
  time.sleep(120)
