import mraa
import time
import sys

if len(sys.argv) < 4:
  print "ERROR: Must provide 3 RGB 0/1 arguments:"
  print "       e.g. 'python battery_rgb.py 0 0 1'"
  sys.exit()

v = map(int, sys.argv[1:])[::-1]

# blue = GP129; green = GP130; red = GP131
bgr = [mraa.Gpio(25), mraa.Gpio(26), mraa.Gpio(35)]

for led in bgr:
  led.dir(mraa.DIR_OUT)
  led.write(0)

i = 0
for led in bgr:
  led.write(v[i])
  time.sleep(.01)
  i += 1
