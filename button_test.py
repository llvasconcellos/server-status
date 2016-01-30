#!/usr/bin/env python

import mraa
import time
import subprocess

pressed = False

def press(args):
  global pressed
  if pressed:
    return
  time.sleep(.1)
  if pin.read() == 1:
    return
  pressed = True
  print('Hold for 10s to power off Edison ')
  i = 0
  while pin.read() == 0:
    i += 1
    time.sleep(.25)
    if i == 50:
      print 'Powering down..'
      subprocess.call("python /home/root/gpio/lcd/report_lines.py 'Shutting down' 'Wait 2 minutes,' 'then flick the' 'power switch.' 'Au revoir!'", shell=True)
      pressed = False
      return
  pressed = False

while True:
  pin = mraa.Gpio(32)
  pin.dir(mraa.DIR_IN)
  pin.isr(mraa.EDGE_BOTH, press, press)
  time.sleep(10800)
  pin.isrExit()

