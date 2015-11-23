import mraa
import time

# red = GP131; green = GP130; blue = GP129
leds = [mraa.Gpio(35), mraa.Gpio(26), mraa.Gpio(25)]

for led in leds:
  led.dir(mraa.DIR_OUT)
  led.write(0)

i = 0
while True:
  leds[i].write(1)
  time.sleep(0.5)
  leds[i].write(0)
  i += 1
  if i == 3:
  	i = 0
