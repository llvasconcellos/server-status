import os
import time
import mraa
import math
import sys

os.chdir('/home/root/gpio')
print time.strftime('%X') + " START"

snooze = 10

## INITIALISE VARIABLES

red = mraa.Gpio(35)     # 'GP131'
red.dir(mraa.DIR_OUT)
green = mraa.Gpio(26)   # 'GP130'
green.dir(mraa.DIR_OUT)
blue = mraa.Gpio(25)    # 'GP129'
blue.dir(mraa.DIR_OUT)

def reset():
  red.write(0)
  green.write(0)
  blue.write(0)

# flash list of LEDs for individual periods and total duration (cycles rounded to multiple of len(leds) )
def flash_colours(leds, duration, period):
  n = len(leds)
  iterations = int(math.floor(float(float(duration) / period) / n + .5) * n)
  for i in range(iterations):
    leds[i%n].write(1)
    time.sleep(period)
    leds[i%n].write(0)
    if n == 1:
      time.sleep(period)

# test LEDs
flash_colours([red, green, blue], 3, .1)
time.sleep(.5)
# explicit order to check pin connections: red, green, blue
flash_colours([red, green, blue], 3, 1)
time.sleep(1)


# Main loop
while True:
  with open('battery_charge.txt', "r") as status_file:
    charge = float(status_file.read())
  reset()
  if charge > 75:
    green.write(1)
    with open('.battery_led_test', "w") as myfile:
      myfile.write(time.strftime('%X') + ' green ' + str(charge) + '\n')
    time.sleep(snooze)
  elif charge > 50:
    blue.write(1)
    with open('.battery_led_test', "w") as myfile:
      myfile.write(time.strftime('%X') + ' blue ' + str(charge) + '\n')
    time.sleep(snooze)
  elif charge > 25:
    red.write(1)
    with open('.battery_led_test', "w") as myfile:
      myfile.write(time.strftime('%X') + ' red ' + str(charge) + '\n')
    time.sleep(snooze)
  elif charge > 0:
    flash_colours([red], snooze, charge/30)
    with open('.battery_led_test', "w") as myfile:
      myfile.write(time.strftime('%X') + ' flashing red ' + str(charge) + '\n')
  else:
    time.sleep(snooze)
    with open('.battery_led_test', "w") as myfile:
      myfile.write(time.strftime('%X') + ' zero charge\n')
  sys.stdout.flush()

