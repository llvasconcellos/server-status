#!/usr/bin/env python

#import sys
import time
#import datetime
import SDL_DS1307
#import os

ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)
now = ds1307.read_datetime()

print "Edison =\t" + time.strftime("%Y-%m-%d %H:%M:%S")
print "DS1307 =\t%s" % now
