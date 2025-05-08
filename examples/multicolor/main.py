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
#   0 show_colors_v
#   1 show_colors_h
#   2 show_image
#   3 blink_leds
#   4 use_buttons

# --- imports   ------------------------------------------------------------

import time
import supervisor
import board
import time
import gc

# --- select DUT and tests   ----------------------------------------------

from inky_imp import InkyImpression673 as Inky
my_tests = [2]
inky = Inky()

# --- main program   ----------------------------------------------------

while not supervisor.runtime.serial_connected:
  time.sleep(1)
print(f"running on board {board.board_id}")

for tst in inky.tests(my_tests):
  print(f"running test: {tst}")
  tst()
  print(f"finished: {tst}",int(time.monotonic()))
  #gc.collect()
  #time.sleep(10)
#inky.deinit()

while True:
  time.sleep(1)
  print("... ",int(time.monotonic()))
