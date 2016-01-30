#!/usr/bin/env python

import mraa
import time
import sys

# switch off all LEDs in group then blink red
# accepts arguments 'battery' and 'server'

leds = [[35,26,25], [31,45,32]] # battery, server

if sys.argv[1] == 'battery':
	leds = leds[0]
elif sys.argv[1] == 'server':
	leds = leds[1]
else:
	sys.exit("must provide 1 argument - string 'battery' or 'server'")

for i in range(len(leds)):
	leds[i] = mraa.Gpio(leds[i])
	leds[i].write(0)

while True:
	leds[0].write(1)
	time.sleep(.05)
	leds[0].write(0)
	time.sleep(2)
