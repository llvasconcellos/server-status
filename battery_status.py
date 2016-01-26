#!/usr/bin/env python

import os
import time
import mraa
import math
import sys
import subprocess

os.chdir('/home/root/gpio')
print time.strftime('%X') + " START"

snooze = 10
charge = -101
subprocess.call('echo 0 > /home/root/debian/home/buendia/battery_shutdown.txt', shell=True)

## INITIALISE VARIABLES

MAX17043_ADDRESS = 0x36
VCELL_REGISTER   = 0x02
SOC_REGISTER     = 0x04
MODE_REGISTER    = 0x06
VERSION_REGISTER = 0x08
CONFIG_REGISTER  = 0x0C
COMMAND_REGISTER = 0xFE
I2C_PORT         = 1
x = mraa.I2c(I2C_PORT)
x.address(MAX17043_ADDRESS)

red = mraa.Gpio(35)     # 'GP131'
red.dir(mraa.DIR_OUT)

# I2C FUNCTIONS

def cellVoltage():
  msb = x.readReg(VCELL_REGISTER)  
  lsb = x.readReg(VCELL_REGISTER+1)
  value = msb << 4 | lsb >> 4
  return (value * .00125)

def stateOfCharge():
  return (x.readReg(SOC_REGISTER) + (x.readReg(SOC_REGISTER+1) / 256))

def reset_i2c():
  x.writeWordReg(COMMAND_REGISTER, 0x0054)
  time.sleep(.3) #spec states 125ms

def quickStart():
  x.writeWordReg(COMMAND_REGISTER, 0x4000)
  time.sleep(.5) #spec states 500ms 

def get_battery_status():
  reset_i2c()
  quickStart()
  charge = stateOfCharge()
  return charge


# flash LED for individual periods and total duration
# includes safeguards for when variablised 'period' exceeds limits and would crash script
def flash_led(led, duration, period):
  period = min(duration, max(.1, float(period)))/2
  iterations = int(math.floor((float(duration) / period) + .5)/2)
  for i in range(iterations):
    led.write(1)
    time.sleep(period)
    led.write(0)
    time.sleep(period)

# test LED
flash_led(red, 3, .1)
time.sleep(1)
k = 0

# Main loop
while True:
  charge_new = get_battery_status()
  try:
    charge_new = int(charge_new)
  except:
    print "Error: failed to convert 'charge' to int " + str(len(charge_new)) + ', string=' + charge_new
  
  # smoothed charge reading
  if charge == -101:
    charge = float(charge_new) # initialise on 1st loop
  else:
    charge = charge * 0.88 + float(charge_new) * 0.12  # ~ avg 12 readings (optimised params)
  
  # output to files
  subprocess.call('echo ' + str(int(charge+.5)) + ' > battery_charge.txt', shell=True)
  subprocess.call('cp battery_charge.txt /home/root/debian/home/buendia/battery_charge.txt', shell=True)
  if k == 0:
    try:
      subprocess.call('cat battery_charge.txt >> sd/logs/battery_charge_log.txt', shell=True)
  k = (k + 1) % 60 # i.e. every 10 mins
  
  if charge <= 5 and not charge < 1: # exception for e.g. disconnected fuel gauge wire
    print "Emergency shutdown: battery=" + str(charge) + "%"
    subprocess.call('echo 1 > /home/root/debian/home/buendia/battery_shutdown.txt', shell=True)
    time.sleep(30)  # time for server to alert tablets
    subprocess.call('poweroff', shell=True)
  
  # light/flash RED LED when battery low
  if charge > 50:
    red.write(0)
    time.sleep(snooze)
  elif charge > 25:
    red.write(1)
    time.sleep(snooze)
  else:
    flash_led(red, snooze, float(charge)/30)
  # any output to file now
  sys.stdout.flush()
