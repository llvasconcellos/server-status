#!/usr/bin/env python

import mraa
import time
import subprocess
import os

pressed = False

def press(args):
  global pressed
  if pressed:
    return
  time.sleep(.1)
  if pin.read() == 1:
    return
  pressed = True
  print('Hold for 5s to power off Edison ')
  subprocess.call("python /home/root/gpio/lcd/report_lines_and_battery.py 'Hold for' '5 seconds' 'to shut down'", shell=True)
  i = 0
  while pin.read() == 0:
    i += 1
    time.sleep(.25)
    if i == 20:
      print 'Powering down..'
      subprocess.call("python /home/root/gpio/lcd/report_lines.py 'Shutting down' 'Wait 2 minutes,' 'then flick the' 'power switch.' 'Au revoir!' &", shell=True)
      subprocess.call('echo 1 > /home/root/debian/home/buendia/battery_shutdown.txt', shell=True)
      time.sleep(30)
      subprocess.call('poweroff', shell=True)
      os._exit
  subprocess.call("python /home/root/gpio/lcd/report_lines_and_battery.py 'Shutdown' 'cancelled'", shell=True)
  pressed = False

pin = mraa.Gpio(32)
pin.dir(mraa.DIR_IN)
pin.isr(mraa.EDGE_BOTH, press, press)
time.sleep(3600)
#pin.isrExit()
