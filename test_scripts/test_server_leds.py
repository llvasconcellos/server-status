import mraa
import time

# red = GP44; green = GP45; blue = GP46
leds = [mraa.Gpio(31), mraa.Gpio(45), mraa.Gpio(32)]

for led in leds:
  led.dir(mraa.DIR_OUT)
  led.write(0)

i = 0
while True:
  leds[i].write(1)
  time.sleep(1)
  leds[i].write(0)
  i += 1
  if i == 3:
    i = 0
