#!/usr/bin/env python

# Update system time from RTC - to run on boot

import time
import SDL_DS1307
import os

print "Edison old =\t" + time.strftime("%Y-%m-%d %H:%M:%S")

ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)
now = ds1307.read_datetime()
date_comd = "date -s '" + str(now) + "'"
os.system(date_comd)

print "DS1307 =\t%s" % now
print "Edison new =\t" + time.strftime("%Y-%m-%d %H:%M:%S")
