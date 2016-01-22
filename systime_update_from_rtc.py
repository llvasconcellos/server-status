#!/usr/bin/env python

#import sys
import time
#import datetime
import SDL_DS1307
import os

print "Edison old =\t" + time.strftime("%Y-%m-%d %H:%M:%S")

ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)
now = ds1307.read_datetime()
date_comd = "date -s '" + str(now) + "'"
os.system(date_comd)

print "DS1307 =\t%s" % now
print "Edison new =\t" + time.strftime("%Y-%m-%d %H:%M:%S")
