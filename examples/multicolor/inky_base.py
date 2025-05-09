# -------------------------------------------------------------------------
# Base class with shared code.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-examples
#
# -------------------------------------------------------------------------

import time
import storage
import sdcardio
import displayio
import terminalio

from adafruit_display_text.bitmap_label import Label
from adafruit_display_shapes.rect import Rect
from digitalio import DigitalInOut, Direction

class InkyBase:

  # --- constructor   -----------------------------------------------------

  def __init__(self,led_gpios,colors,dither=False):
    """ constructor """

    self.duration = 0.5
    self._leds = []
    for gpio in led_gpios:
      led = DigitalInOut(gpio)
      led.direction = Direction.OUTPUT
      self._leds.append(led)

    self._palette = displayio.Palette(len(colors),dither=dither)
    print("Palette:")
    for index,color in enumerate(colors):
      self._palette[index] = color
      print(f"  {index}: {color:06X}")

  # --- free resources   ---------------------------------------------------

  def deinit(self):
    """ free resources """
    pass

  # --- update the display   -----------------------------------------------
  
  def update(self,g):
    """ update the display """

    self.display.root_group = g

    print(f"waiting for time-to-refresh: {self.display.time_to_refresh}s")
    time.sleep(self.display.time_to_refresh)

    print("refreshing...:")
    start = time.monotonic()
    self.display.refresh()
    duration = time.monotonic()-start
    print(f"display (refreshed): {duration:f}s")

  # --- mount SD   --------------------------------------------------------

  def _mount_sd(self):
    """ mount SD """

    try:
      sdcard = sdcardio.SDCard(self._spi,self._cs_pin_sd,1_000_000)
      vfs = storage.VfsFat(sdcard)
      storage.mount(vfs, "/sd")
    except:
      print("failed to mount SD, using internal /sd directory")

  # --- blink a single LED   ---------------------------------------------

  def blink(self,led):
    """ blink LED """

    led.value = 1
    time.sleep(self.duration)
    led.value = 0
    time.sleep(self.duration)

  # --- blink all LEDs   -------------------------------------------------

  def blink_leds(self):
    """ blink LEDs of display """

    # one LED at a time
    for led in self._leds:
      self.blink(led)

    # all LED together
    for led in self._leds:
      led.value = 1
    time.sleep(self.duration)
    for led in self._leds:
      led.value = 0
    time.sleep(self.duration)

  # --- colors and texts (vertical)   ---------------------------------------

  def show_colors_v(self):
    """ show vertical stripes """

    g = displayio.Group()
    stripe_width = self.display.width // len(self._palette)
    for i in range(len(self._palette)):
      rect = Rect(x=i*stripe_width,y=0,
                  width=stripe_width,height=self.display.height,
                  fill=self._palette[i],outline=None,stroke=0)
      g.append(rect)

    lbl = Label(terminalio.FONT, text=self._title, color=0xFFFFFF, scale=3)
    lbl.anchor_point = (0.5, 0.5)
    lbl.anchored_position = (self.display.width // 2, self.display.height // 3)
    g.append(lbl)
    self.update(g)

  # --- colors and texts (horizontal)   -------------------------------------

  def show_colors_h(self):
    """ show horizontal stripes """

    g = displayio.Group()
    stripe_height = self.display.height // 7
    for i in range(len(self._palette)):
      rect = Rect(x=0,y=i*stripe_height,
                  width=self.display.width,height=stripe_height,
                  fill=self._palette[i],outline=None,stroke=0)
      g.append(rect)

    lbl = Label(terminalio.FONT, text=self._title, color=0xFFFFFF, scale=3)
    lbl.anchor_point = (0.5, 0.5)
    lbl.anchored_position = (self.display.width // 2, self.display.height // 2)
    g.append(lbl)
    self.update(g)

  # --- show image from SD   ---------------------------------------------

  def show_image(self):
    """ load and show image """

    self._mount_sd()

    # create with:
    # convert netscape: -resize 'widthxheight!' colors-widthxheight.bmp
    f = open(f"/sd/image-{self.display.width}x{self.display.height}.bmp",
             "rb")
    g = displayio.Group()
    pic = displayio.OnDiskBitmap(f)
    t = displayio.TileGrid(pic, pixel_shader=self._palette)
    g.append(t)
    self.update(g)
    f.close()

  # --- use buttons   -----------------------------------------------------

  def use_buttons(self):
    """ use buttons and blink corresponding LED """

    pad, led_index = self.keypad()

    queue = pad.events
    queue.clear()
    print("press any button:")
    while True:
      if not len(queue):
        time.sleep(0.1)
        continue
      ev = queue.get()
      print(f"pressed key {ev.key_number}")
      self.blink(self._leds[led_index[ev.key_number]])

  # --- list of supported/selected tests   -----------------------------------

  def tests(self,selected):
    """ return list of supported tests """

    all_tests = [
      self.show_colors_v,
      self.show_colors_h,
      self.show_image,
      self.blink_leds,
      self.use_buttons
    ]

    sel_tests = []
    for index, test in enumerate(all_tests):
      if index in selected:
        sel_tests.append(test)
    return sel_tests
