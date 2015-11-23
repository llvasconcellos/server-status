import mraa
import time

# b1, g1, r1, b2, g2, r2
leds = [32,45,31,25,26,35]

for i in range(6):
  leds[i] = mraa.Gpio(leds[i])
  leds[i].dir(mraa.DIR_OUT)

for led in leds:
  led.write(0)
  time.sleep(.01)
