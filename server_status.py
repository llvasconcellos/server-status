#!/usr/bin/env python

import subprocess
import os
import time
import inspect
import sys
import math
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from re import sub

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

current_lcd_lines = []

# Edison software SPI config:
SCLK = 35 # 10
DIN  = 26 # 11
DC   = 25 # 32
RST  = 45 # 46
CS   = 31 # 23

font = ImageFont.truetype('fonts/Minecraftia-Regular.ttf', 8)

# new line positions
h = [-2,6,14,22,30,38]

# reset openmrs internal status to match openmrs_int
subprocess.call('echo -1 > /home/root/debian/home/buendia/server_status.txt', shell=True)


## FUNCTIONS

# Report lines to LCD
def report_lcd(lines):
  global current_lcd_lines
  current_lcd_lines = lines
  with open('contrast.txt', "r") as f:
    contrast = int(sub('\\n', '', f.read()))
  disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
  disp.begin(contrast = contrast)
  image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
  draw = ImageDraw.Draw(image)
  draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
  for i, line in enumerate(lines):
    if i < 5:
      draw.text((0, h[i]), line, font=font)
  # Battery bar
  Y = 40    # vertical position
  with open('battery_charge.txt', "r") as f:
    charge_val = int(f.read())
  charge = int(50 * (float(charge_val) / 100))
  draw.polygon([(0,1+Y), (2,1+Y), (2,0+Y), (4,0+Y), (4,1+Y), (6,1+Y), (6,7+Y), (0,7+Y)], outline=0, fill=255)
  if charge_val == 101:
    draw.text((12,Y-1), 'wait..', font=font)
  elif charge_val == 0:
    draw.text((12,Y-1), 'not reporting', font=font)
  else:
    draw.text((61,Y-1), str(charge_val) + '%', font=font)
    draw.rectangle((9, Y+1, 9+50, 7+Y), outline=0, fill=255)
    draw.rectangle((9, Y+1, 9+charge, 7+Y), outline=0, fill=0)
  disp.image(image)
  disp.display()

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
    report_lcd(['ERR: openmrs int.','status is non-numeric','server_status.txt'])
    time.sleep(60)
    return
  if not openmrs_int_new == openmrs_int:  # state has changed
    report('openmrs_int change: ' + str(openmrs_int) + ' > ' + str(openmrs_int_new))
    openmrs_int = openmrs_int_new
    ## REPORT NEW STATUS
    if openmrs_int == 0:                 # 0 = down (Not implemented)
      report_lcd(['SYSTEM DOWN'])
    elif openmrs_int == 1:               # 1 = normal use
      report_lcd(['System OK'])
    elif openmrs_int == 2:               # 2 = back-up internally: processing
      report_lcd(['Backing up (SD)...'])
    elif openmrs_int == 3:               # 3 = back-up to USB: processing
      report_lcd(['Backing up (USB)...'])
    elif openmrs_int == 4:               # 4 = back-up: failed
      report_lcd(['BACKUP FAILED'])
    elif openmrs_int == 5:               # 5 = restoring from backup
      report_lcd(['Restoring...'])
    elif openmrs_int == 6:               # 6 = restore failed
      report_lcd(['RESTORE FAILED'])
    elif openmrs_int == 7:               # 7 = updating
      report_lcd(['Updating...'])
    elif openmrs_int == 8:               # 8 = update failed
      report_lcd(['UPDATE FAILED'])
    elif openmrs_int == 2001:            # 2001 = open the pod bay doors
      report_lcd(['I\'m sorry, Dave'])

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
#     no - sleep for ?s
#     yes - change state to detected
#   yes - has OpenMRS been detected yet?
#     no - is it up now?
#       no - sleep for ?s
#       yes - change state to detected
#     yes - has minute passed since last external check?
#       no - check OpenMRS internal status & report any changes
#       yes - has OpenMRS stopped responding to ping?
#         yes - report

report_lcd(['SYSTEM BOOTING'])

print '*** START MAIN LOOP ***'
k = 0

while True:
  k = (k + 1) % 60
  if buendia == 0:
    # STAGE 1: Buendia not running. Ping for response
    buendia_status = check_url(buendia_url)
    buendia_new = buendia_status[0]
    if buendia_new > 0:
      # STAGE 2: Buendia detected
      buendia = 1                               # [possible bug if openmrs_internal_status returned code 2..]
      report()
      report_lcd(['LOADING OPENMRS'])
    else:
      time.sleep(10)                            # LED is red so just sleep
  else:                                         # Buendia is running
    if openmrs_ext == 0:                        # has OpenMRS not been detected yet?
      openmrs_status = check_url(openmrs_url)   # Ping OpenMRS for response
      openmrs_new = openmrs_status[0]
      if k == 0:
        report_lcd(current_lcd_lines)
      if openmrs_new != 0:                      # OpenMRS not detected
        # STAGE 3: OpenMRS detected
        openmrs_ext = 1                         # [possible bug if openmrs_internal_status returned code 2..]
        report()
        report_lcd(['SYSTEM O.K.'])
    else:                                       # OpenMRS is running
      if time.time() - last_check < 60:         # less than minute since last status check?
        openmrs_internal_status()
      else:                                     # a minute has passed
        report('minute check')
        report_lcd(current_lcd_lines)           # refresh LCD for battery level
        openmrs_status = check_url(openmrs_url) # ping OpenMRS again
        openmrs_new = openmrs_status[0]
        if openmrs_new == 0:                    # cannot detect OpenMRS anymore
          # we could have a server problem. Report and step back to system boot phase
          openmrs_ext = 0
          report()
          report_lcd(['OPENMRS DOWN','at ' + time.strftime("%H:%M", time.gmtime()) + 'OpenMRS', 'down: wait 10 min &','Reboot if not up.','See syslog.'])
  sys.stdout.flush()                            # output to file now
  time.sleep(1)

