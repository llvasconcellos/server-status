# import math
# import time
# import Adafruit_Nokia_LCD as LCD
# import Adafruit_GPIO.SPI as SPI
# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw

# Edison software SPI config:
# SCLK = 10
# DIN = 11
# DC = 32 # 36
# RST = 46 # 48
# CS = 23
# disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Edison hardware SPI config:
DC = 32 #32 #36 #46
RST = 46 #46 #48 #47
SPI_PORT = 5
SPI_DEVICE = 1
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

disp.begin(contrast=40)
disp.clear()
disp.display()

image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
font = ImageFont.load_default()
draw.text((0,0), 'One ha ha ha', font=font)
draw.text((0,12), 'Two ha ha ha', font=font)
draw.text((0,24), 'Three ha ha', font=font)
draw.text((0,36), 'Five! SIX!', font=font)

disp.image(image)
disp.display()
