import os
import time
import mraa
import math
import sys

os.chdir('/home/root/gpio')
print time.strftime('%X') + " START"

snooze = 10

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
green = mraa.Gpio(26)   # 'GP130'
green.dir(mraa.DIR_OUT)
blue = mraa.Gpio(25)    # 'GP129'
blue.dir(mraa.DIR_OUT)


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


# LED FUNCTIONS

def reset():
  red.write(0)
  green.write(0)
  blue.write(0)

# flash list of LEDs for individual periods and total duration (cycles rounded to multiple of len(leds) )
def flash_colours(leds, duration, period):
  n = len(leds)
  iterations = int(math.floor(float(float(duration) / period) / n + .5))
  iterations = max(1, iterations if n>1 else iterations/2)
  for i in range(iterations):
    for led in leds:
      led.write(1)
      time.sleep(period)
      led.write(0)
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
  charge = get_battery_status()
  with open('battery_charge.txt', "w") as myfile:
    myfile.write(str(charge) + '\n')
  try:
    charge = int(charge)
  except:
    print "Error: failed to convert 'charge' to int " + str(len(charge)) + ', string=' + charge
  if charge <= 5:
    print "Emergency shutdown: battery=" + str(charge) + "%"
    subprocess.call('poweroff', shell=True)
  reset()
  if charge > 75:
    green.write(1)
  elif charge > 50:
    blue.write(1)
  elif charge > 25:
    red.write(1)
  elif charge > 0:
    flash_colours([red], snooze, charge/30)
  if charge > 25 or charge <= 0:
    time.sleep(snooze)
  sys.stdout.flush()

