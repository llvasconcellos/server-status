import mraa
import time
import os
import sys

os.chdir('/home/root/gpio')
print time.strftime('%X') + " START"

MAX17043_ADDRESS = 0x36
VCELL_REGISTER   = 0x02
SOC_REGISTER     = 0x04
MODE_REGISTER    = 0x06
VERSION_REGISTER = 0x08
CONFIG_REGISTER	 = 0x0C
COMMAND_REGISTER = 0xFE
I2C_PORT         = 1

def cellVoltage():
  msb = x.readReg(VCELL_REGISTER)  
  lsb = x.readReg(VCELL_REGISTER+1)
  value = msb << 4 | lsb >> 4
  return (value * .00125)

def stateOfCharge():
  return (x.readReg(SOC_REGISTER) + (x.readReg(SOC_REGISTER+1) / 256))

def reset():
  x.writeWordReg(COMMAND_REGISTER, 0x0054)
  time.sleep(.3) #spec states 125ms

def quickStart():
  x.writeWordReg(COMMAND_REGISTER, 0x4000)
  time.sleep(.5) #spec states 500ms 

x = mraa.I2c(I2C_PORT)
x.address(MAX17043_ADDRESS)

while True:
  reset()
  quickStart()
  charge = stateOfCharge()
  sys.stdout.flush()
  with open('battery_charge.txt', "w") as myfile:
    myfile.write(str(charge) + '\n')
  time.sleep(10)
