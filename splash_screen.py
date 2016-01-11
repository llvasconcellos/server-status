import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from re import sub

# Edison software SPI config:
SCLK = 10
DIN = 11
DC = 32
RST = 46
CS = 23
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

with open('contrast.txt', "r") as f:
  contrast = int(sub('\\n', '', f.read()))

disp.begin(contrast = contrast)
image = Image.open('splash.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
draw = ImageDraw.Draw(image)
disp.image(image)
disp.display()
