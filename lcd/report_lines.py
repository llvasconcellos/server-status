#!/usr/bin/env python

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
from random import shuffle
from re import sub

# Edison software SPI config:
SCLK = 35 # 10
DIN  = 26 # 11
DC   = 25 # 32
RST  = 45 # 46
CS   = 31 # 23

disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

with open('/home/root/gpio/contrast.txt', "r") as f:
  contrast = int(sub('\\n', '', f.read()))

disp.begin(contrast = contrast)
disp.clear()

font = ImageFont.truetype('/home/root/gpio/fonts/Minecraftia-Regular.ttf', 8)
#font = ImageFont.load_default()

# new line positions
h = [-2,6,14,22,30,38]

# initialise
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

# report lines
n = min(6, len(sys.argv)-1)
for i in range(n):
  draw.text((0,h[i]+0), sys.argv[i+1], font=font)

disp.image(image)
disp.display()


