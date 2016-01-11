import subprocess
import os
import time
import inspect
import sys
import math

os.chdir('/home/root/gpio')
print time.strftime('%X') + " START"

## INITIALISE VARIABLES

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
def report(msg=''):
  line = inspect.currentframe().f_back.f_lineno
  print time.strftime('%X') + ' - line ' + str(line) +' '+msg

def openmrs_internal_status():
  global openmrs_int
  with open('/home/root/debian/home/buendia/server_status.txt', "r") as status_file:
    new_status = status_file.read()
  try:
    openmrs_int_new = int(float(new_status))
  except:
    print "Error: poss non-numeric content in /debian/home/buendia/server_status.txt: " + new_status
    openmrs_int_new = openmrs_int      # this is to stop the script from crashing
  if not openmrs_int_new == openmrs_int:  # state has changed
    report('openmrs_int change: ' + str(openmrs_int) + ' > ' + str(openmrs_int_new))
    openmrs_int = openmrs_int_new
    ## REPORT NEW STATUS
  # TASK LED's according to OpenMRS server status
  if openmrs_int == 0:                 # down
    # REPORT
  elif openmrs_int == 1:               # normal use
    # REPORT
  elif openmrs_int == 2:               # back-up: started
    # REPORT
  elif openmrs_int == 3:               # back-up: processing
    # REPORT
  elif openmrs_int == 4:               # back-up: failed
    # REPORT
  elif openmrs_int == 5:               # update: checking
    # REPORT
  elif openmrs_int == 6:               # update: updating
    # REPORT
  elif openmrs_int == 7:               # update: failed
    # REPORT
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


## STATUS CODES
# 0 - down
# 1 - running
# 2 - activity
# 3 - backing-up
# 4 - backup failed


## MAIN LOOP

## LOGIC SUMMARY
# has Buendia been detected yet (external check)?
#   no - is it up now?
#     no - sleep for 5s
#     yes - change state to detected
#   yes - has OpenMRS been detected yet?
#     no - is it up now?
#       no - sleep for 5s
#       yes - change state to detected
#     yes - has minute passed since last external check?
#       no - check OpenMRS internal status & report any changes
#       yes - has OpenMRS stopped responding to ping?
#         yes - report


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
      buendia = 1                               # [possible bug if openmrs_internal_status returned code 2..]
      report()
      reset()
    else:
      time.sleep(10)                            # LED is red so just sleep
  else:                                         # Buendia is running
    if openmrs_ext == 0:                        # has OpenMRS not been detected yet?
      openmrs_status = check_url(openmrs_url)   # Ping OpenMRS for response
      openmrs_new = openmrs_status[0]
      if openmrs_new == 0:                      # OpenMRS not detected
        flash_colours([red, green], 10, .2)
      else:                                     # OpenMRS detected
        # STAGE 3: OpenMRS detected
        openmrs_ext = 1                         # [possible bug if openmrs_internal_status returned code 2..]
        report()
        reset()
        green.write(1)
    else:                                       # OpenMRS is running
      if time.time() - last_check < 60:         # less than minute since last status check?
        openmrs_internal_status()
      else:                                     # a minute has passed
        report('minute check')
        openmrs_status = check_url(openmrs_url) # ping OpenMRS again
        openmrs_new = openmrs_status[0]
        if openmrs_new == 0:                    # cannot detect OpenMRS anymore
          # we could have a server problem, so do not update 'openmrs_ext' but blink RED instead
          report()
          reset()
          flash_colours([red], 60, .5)          # 60 seconds (i.e. time to next external check)
        else:
          green.write(1)
  sys.stdout.flush()                            # output to file now
