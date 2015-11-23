import mraa
import time
import sys

if len(sys.argv) < 4:
  print "ERROR: Must provide 3 RGB 0/1 arguments:"
  print "       e.g. 'python server_rgb.py 0 0 1'"
  sys.exit()

v = map(int, sys.argv[1:])[::-1]

# blue = GP46; green = GP45; red = GP44
bgr = [mraa.Gpio(32), mraa.Gpio(45), mraa.Gpio(31)]

for led in bgr:
  led.dir(mraa.DIR_OUT)
  led.write(0)

i = 0
for led in bgr:
  led.write(v[i])
  time.sleep(.01)
  i += 1
