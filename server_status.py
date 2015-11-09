import subprocess
import os
import time
import mraa
import inspect
import sys

os.chdir('/home/root/gpio')
print "*** START server_status.py ***"

# FUNCTIONS

# Returns current line number
def lineno(): 
    return inspect.currentframe().f_back.f_lineno

def red_on():
  global red
  if not red:
    print "red on"
    red = True
    red_led.write(1)

def red_off():
  global red
  if red:
    print "red off"
    red = False
    red_led.write(0)

def green_on():
  global green
  if not green:
    print "green on"
    green = True
    green_led.write(1)

def green_off():
  global green
  if green:
    print "green off"
    green = False
    green_led.write(0)

def blue_on():
  global blue
  if not blue:
    blue = True
    print "blue on"
    blue_led.write(1)

def blue_off():
  global blue
  if blue:
    print "blue off"
    blue = False
    blue_led.write(0)

def reset():
  global red
  global green
  global blue
  if red:
    red_off()
  if green:
    green_off()
  if blue:
    blue_off()


def get_openmrs_internal_status():
  with open('/home/root/debian/home/buendia/server_status.txt', "r") as status_file:
    status = status_file.read()
    return int(status)

def report(n):
  print time.strftime('%X') + ' - line ' + str(n+1)

def openmrs_internal_status():
  global openmrs_i
  openmrs_i_new = get_openmrs_internal_status()
  if not openmrs_i_new == openmrs_i:
    reset()
    openmrs_i = openmrs_i_new
  # TASK LED's according to status
  if openmrs_i == 0:       # down - GREEN on
    report(lineno())
    reset()
    report(lineno())
    green_on()
  elif openmrs_i == 1:     # normal use - BLUE on
    report(lineno())
    reset()
    report(lineno())
    blue_on()
  elif openmrs_i == 2:     # activity  - blink BLUE on/off
    if blue:
      report(lineno())
      blue_off()
    else:
      report(lineno())
      blue_on()
  elif openmrs_i == 3:     # backing-up - blink BLUE/GREEN
    if blue:
      report(lineno())
      blue_off()
      report(lineno())
      green_on()
    else:
      report(lineno())
      green_off()
      report(lineno())
      blue_on()
  elif openmrs_i == 4:     # back-up failed - blink BLUE/RED
    if blue:
      report(lineno())
      blue_off()
      report(lineno())
      red_on()
    else:
      report(lineno())
      red_off()
      report(lineno())
      blue_on()

# classify server repsonses - i.e. interpret top line of 'curl -Is <url>'
def classify_status(sts):
  if sts == '':               # no response
    return 0
  elif sts.find('200') > -1:  # positive response
    return 1
  else: # other response (e.g. redirected) [Might have to debug this..]
    return 2


# INITIALISE SETTINGS

red = False
red_led = mraa.Gpio(31)     # 'GP44'
red_led.dir(mraa.DIR_OUT)

green = False
green_led = mraa.Gpio(45)   # 'GP45'
green_led.dir(mraa.DIR_OUT)

blue = False
blue_led = mraa.Gpio(32)    # 'GP46'
blue_led.dir(mraa.DIR_OUT)

# test LEDs
report(lineno())

for i in range(15):
  red_on()
  time.sleep(.05)
  reset()
  green_on()
  time.sleep(.05)
  reset()
  blue_on()
  time.sleep(.05)
  reset()

time.sleep(1)
red_on()

buendia = 0     # localhost status
openmrs = 0     # openmrs server status
openmrs_i = -1  # openmrs internal status
last_check = time.time()

# reset openmrs internal status
subprocess.call('echo -1 > /home/root/debian/home/buendia/server_status.txt', shell=True)


## STATUS CODES
# 0 - down
# 1 - running
# 2 - activity
# 3 - backing-up
# 4 - backup failed

## LOGIC
# is openmrs already up?
#   yes: is new minute? (check status every minute)
#     yes: is openmrs still up? (ie. status>0)
#       yes: report openmrs internal status
#       no: flashing RED
#     no: report openmrs internal status
#   no: is buendia already up?
#     yes: is openmrs up now?
#         yes: BLUE & update openmrs
#         no: nothing
#     no: is buendia up now?
#         yes: GREEN & update buendia
#         no: stay RED


# MAIN LOOP

print '*** START MAIN LOOP ***'

while True:
  if time.time() - last_check > 10800:  # truncate log file every 3 hours # 10800
    subprocess.call("tail -1000 sd/log.txt > sd/log.tmp; echo '' > sd/log.txt; cat sd/log.tmp >> sd/log.txt; rm sd/log.tmp", shell=True)
  if openmrs > 0:                       # OpenMRS already reported running
    if time.time() - last_check > 60:   # has a minute passed since last status check?
      # external check that OpenMRS is running
      openmrs_status = subprocess.check_output("curl --max-time 2 -Is localhost:9000/openmrs/index.htm | head -n 1", shell=True)
      openmrs_new = classify_status(openmrs_status)
      last_check = time.time()
      if openmrs_new == 0:              # OpenMRS says server has gone down
        reset()
        for i in range(60):             # blink for 30s then re-check  *** BUG ***
          if red:
            report(lineno())
            red_off()
          else:
            report(lineno())
            red_on()
          time.sleep(1)
      else:                             # server still up
        openmrs_internal_status()
    else:                               # Minute has not passed. Run an internal status check
      openmrs_internal_status()
    time.sleep(1)
  else:                                 # OpenMRS not yet reported running
    if buendia > 0:                     # Buendia already reported running
      # external check that OpenMRS is running
      openmrs_status = subprocess.check_output("curl --max-time 2 -Is localhost:9000/openmrs/index.htm | head -n 1", shell=True)
      openmrs_new = classify_status(openmrs_status)
      last_check = time.time()
      if openmrs_new > 0:
        openmrs = 1                     # OpenMRS is now up [possibly wrong if classify_status returned code 2..]
        report(lineno())
        reset()
        report(lineno())
        blue_on()
      else:                             # i.e. openmrs_new == 0
        openmrs = 0
    else:                               # Buendia not yet reported running
      # external check that Buendia is running
      buendia_status = subprocess.check_output("curl --max-time 2 -Is localhost | head -n 1", shell=True)
      buendia_new = classify_status(buendia_status)
      if buendia_new > 0:
        buendia = 1                     # Buendia is now up [possibly wrong if classify_status returned code 2..]
        report(lineno())
        reset()
        report(lineno())
        green_on()
    time.sleep(10)
  sys.stdout.flush()                    # send this loop's reporting to file now

