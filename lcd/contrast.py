#!/usr/bin/env python

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from re import sub
import sys

# Edison software SPI config:
SCLK = 35 # 10
DIN  = 26 # 11
DC   = 25 # 32
RST  = 45 # 46
CS   = 31 # 23
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

if len(sys.argv) > 1:
  contrast = int(sys.argv[1])
  with open('contrast.txt', "w") as f:
    f.write(str(contrast))
else:
  with open('contrast.txt', "r") as f:
    contrast = int(sub('\\n', '', f.read()))

disp.begin(contrast = contrast)
