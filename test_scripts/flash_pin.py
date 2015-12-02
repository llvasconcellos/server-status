import mraa
import time
import sys

if len(sys.argv) < 2:
  print "ERROR: Must provide an MRAA pin number argument:"
  print "       e.g. 'python flash_pin.py 32'"
  sys.exit()

led = mraa.Gpio(int(sys.argv[1]))

while True:
  led.write(1)
  time.sleep(2)
  led.write(0)
  time.sleep(2)
