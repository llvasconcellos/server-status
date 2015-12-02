import subprocess
import os
import time
import mraa
import inspect
import sys
import math

os.chdir('/home/root/gpio')
print time.strftime('%X') + " START"

## INITIALISE VARIABLES

red = mraa.Gpio(31)     # 'GP44'
red.dir(mraa.DIR_OUT)
green = mraa.Gpio(45)   # 'GP45'
green.dir(mraa.DIR_OUT)
blue = mraa.Gpio(32)    # 'GP46'
blue.dir(mraa.DIR_OUT)

buendia     = 0   # localhost status
openmrs_ext = 0   # openmrs server status
openmrs_int = -1  # openmrs internal status
buendia_url = 'localhost'
openmrs_url = 'localhost:9000/openmrs/index.htm'

last_check = time.time()
last_led_check = time.time()

# reset openmrs internal status to match openmrs_int
subprocess.call('echo -1 > /home/root/debian/home/buendia/server_status.txt', shell=True)


## FUNCTIONS

# Returns next line number (debugging)
def report():
  line = inspect.currentframe().f_back.f_lineno
  print time.strftime('%X') + ' - line ' + str(line + 1)

def reset():
  red.write(0)
  green.write(0)
  blue.write(0)

# modulates LED to reduce power consumption (necessary to meet GPIO TXB0108 module's output)
def light(led, period):
  for i in range(max(int((period/0.018)+.5), 1)):
    led.write(1)
    time.sleep(.008)
    led.write(0)
    time.sleep(.01)

# flash list of LEDs for individual periods and total duration (cycles rounded to multiple of len(leds) )
def flash_colours(leds, duration, period):
  n = len(leds)
  iterations = int(math.floor(float(float(duration) / period) / n + .5) * n)
  for i in range(iterations):
    light(leds[i%n], period)
    if n == 1:
      time.sleep(period)

def openmrs_internal_status(): # runs for ~1 second regardless of state
  global openmrs_int
  with open('/home/root/debian/home/buendia/server_status.txt', "r") as status_file:
    openmrs_int_new = int(status_file.read())
  if not openmrs_int_new == openmrs_int:  # state has changed
    print time.strftime('%X') + ' - openmrs_int change: ' + str(openmrs_int) + ' > ' + str(openmrs_int_new)
    reset()
    openmrs_int = openmrs_int_new
  # TASK LED's according to OpenMRS server status
  if openmrs_int == 0:       # down - flash RED
    flash_colours([red], 1, .5)
  elif openmrs_int == 1:     # normal use - BLUE on
    light(blue, 1)
  elif openmrs_int == 2:     # back-up: started  - blink BLUE slow
    flash_colours([blue], 1, .5)
  elif openmrs_int == 3:     # back-up: processing - blink BLUE fast
    flash_colours([blue], 1, .1)
  elif openmrs_int == 4:     # back-up: failed - blink BLUE/RED slow
    flash_colours([blue, red], 1, .5)
  elif openmrs_int == 5:     # update: checking - blink GREEN slow
    flash_colours([green], 1, .5)
  elif openmrs_int == 6:     # update: updating - blink GREEN fast
    flash_colours([green], 1, .1)
  elif openmrs_int == 7:     # update: failed - blink GREEN/RED slow
    flash_colours([green, red], 1, .5)
  else:
    time.sleep(1)

# classify server repsonses - i.e. interpret top line of 'curl -Is <url>'
def check_url(url):
  global last_check
  response = subprocess.check_output("curl --max-time 1 -Is " + url + " | head -n 1", shell=True)
  if url == openmrs_url:
    report()
    last_check = time.time()
  if response == '':               # no response
    return [0, response]
  elif response.find('200') > -1:  # positive response
    return [1, response]
  else:                            # other response (e.g. redirected) [Might have to debug this..]
    return [2, response]


# Test LEDs, then RED on
flash_colours([red, green, blue], 3, .1)
time.sleep(.5)
# slow flash in explicit order to confirm pin connections
flash_colours([red, green, blue], 3, 1)
time.sleep(1)
red.write(1)

## STATUS CODES
# 0 - down
# 1 - running
# 2 - activity
# 3 - backing-up
# 4 - backup failed


## MAIN LOOP

## LOGIC SUMMARY
# has Buendia been detected yet?
#   no - is it up now?
#     no - sleep for 5s
#     yes - change state to detected
#   yes - has OpenMRS been detected yet?
#     no - is it up now?
#       no - flash RED/BLUE for 5s
#       yes - change state to detected & BLUE on
#     yes - has minute passed since last external check?
#       no - check OpenMRS internal status & report accordingly
#       yes - has OpenMRS stopped responding to ping?
#         yes - flash RED for 60s till next ping check


print '*** START MAIN LOOP ***'

while True:
  # safeguard in case LEDs all go off
  if time.time() - last_led_check > 60:
    last_led_check = time.time()
    if sum( [red.read(), green.read(), blue.read()] ) == 0:
      buendia = 0
      openmrs_ext = 0
      red.write(1)
  if buendia == 0:
    # STAGE 1: Buendia not running. Ping for response
    buendia_status = check_url(buendia_url)
    buendia_new = buendia_status[0]
    if buendia_new > 0:
      # STAGE 2: Buendia detected
      buendia = 1                               # [possible bug if classify_status returned code 2..]
      report()
      reset()
    else:
      time.sleep(10)                            # LED is red so just sleep
  else:                                         # Buendia is running
    if openmrs_ext == 0:                        # has OpenMRS not been detected yet?
      openmrs_status = check_url(openmrs_url)   # Ping OpenMRS for response
      openmrs_new = openmrs_status[0]
      if openmrs_new == 0:                      # OpenMRS not detected
        flash_colours([red, blue], 10, .2)
      else:                                     # OpenMRS detected
        # STAGE 3: OpenMRS detected
        openmrs_ext = 1                         # [possible bug if classify_status returned code 2..]
        report()
        reset()
        blue.write(1)
    else:                                       # OpenMRS is running
      if time.time() - last_check < 60:         # less than minute since last status check?
        openmrs_internal_status()
      else:                                     # a minute has passed
        report()
        openmrs_status = check_url(openmrs_url) # ping OpenMRS again
        openmrs_new = openmrs_status[0]
        if openmrs_new == 0:                    # cannot detect OpenMRS anymore
          # we could have a server problem, so do not update 'openmrs_ext' but blink RED instead
          report()
          reset()
          flash_colours([red], 60, .5)          # 60 seconds (i.e. time to next external check)
  sys.stdout.flush()                            # output to file now
