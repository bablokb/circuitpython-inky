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
my_tests = [("fill",0xFF0000), ("black",), ("white",)]

# --- imports   ------------------------------------------------------------

import time
import board
import time
import gc

# --- select DUT and tests   ----------------------------------------------

from inky_imp import InkyImpression57 as Inky

# --- main program   ----------------------------------------------------

time.sleep(10)
print(f"running on board {board.board_id}")
inky = Inky()

for tst in my_tests:
  start = time.monotonic()
  test, *args = tst
  print(f"[{start:0.1f}] starting: {test}({args})")
  getattr(inky,test)(*args)
  end = time.monotonic()
  print(f"[{end:0.1f}] finished: {test}({args}) (duration: {end-start:0.1f})")
  gc.collect()

  # wait the configured time-to-refresh
  ttr = inky.display.time_to_refresh
  if ttr:
    start = time.monotonic()
    print(f"[{start:0.1f}] waiting {ttr}s")
    time.sleep(ttr)
    end = time.monotonic()
    print(f"[{end:0.1f}] finished waiting")
#inky.deinit()

while True:
  time.sleep(1)
  print("... ",int(time.monotonic()))
