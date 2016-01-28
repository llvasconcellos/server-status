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
  print('Hold for 10s to power off Edison ')
  i = 0
  while pin.read() == 0:
    i += 1
    time.sleep(.25)
    if i == 40:
      print 'Powering down..'
      subprocess.call('poweroff', shell=True)
      os._exit
  pressed = False

while True:
  pin = mraa.Gpio(13)
  pin.dir(mraa.DIR_IN)
  pin.isr(mraa.EDGE_BOTH, press, press)
  time.sleep(10800)
  pin.isrExit()

