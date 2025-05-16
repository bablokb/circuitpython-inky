# -------------------------------------------------------------------------
# Testprogram for Pimoroni's InkyImpression/InkyFrame displays
#
# The Impression-displays are for a Pi and to run it with something else,
# you need either additional wiring or an adapter (e.g. from
# https://github.com/bablokb/pcb-pico-pi-base)
#
# Author: Bernhard Bablok
# License: MIT
#
# Website: https://github.com/bablokb/circuitpython-inky
# -------------------------------------------------------------------------

# Tests:
TESTS = [
  "show_colors_v",
  "show_colors_h",
  "show_image",
  "blink_leds",
  "use_buttons",
  "fill",
  "black",
  "white",
  ]

# selected tests: list of (test,args)
my_tests = [("show_image",), ("black",), ("white",)]

# --- imports   ------------------------------------------------------------

import time
import board
import time
import gc
import atexit

# --- select DUT   --------------------------------------------------------

from inky_imp import InkyImpression57 as Inky

border_color = None
#from inky.acep7 import GREEN as border_color
inky_args = {
  "border_color": border_color,
#  "busy_pin": None,
#  "refresh_time": 12,
  }

# --- exit processing   ------------------------------------------------------

def at_exit(inky):
  """ release displays and free SPI-bus """

  print("atexit: deinit ressources")
  inky.deinit()

# --- main program   ----------------------------------------------------

time.sleep(5)
print(f"running on board {board.board_id}")
inky = Inky(**inky_args)

atexit.register(at_exit,inky)

for tst in my_tests:
  start = time.monotonic()
  test, *args = tst
  print(f"[{start:0.1f}] starting: {test}({args})")
  getattr(inky,test)(*args)
  end = time.monotonic()
  print(f"[{end:0.1f}] finished: {test}({args}) (duration: {end-start:0.1f})")
  gc.collect()

while True:
  time.sleep(1)
  print("... ",int(time.monotonic()))
