#!/usr/bin/env python

import mraa
import time

leds = [32,45,31,25,26,35]

for i in range(6):
  leds[i] = mraa.Gpio(leds[i])
  leds[i].dir(mraa.DIR_OUT)

for led in leds:
  led.write(1)
  time.sleep(.01)
