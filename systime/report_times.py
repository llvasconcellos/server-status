#!/usr/bin/env python

# Report system and RTC times

import time
import SDL_DS1307

ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)
now = ds1307.read_datetime()

print "Edison =\t" + time.strftime("%Y-%m-%d %H:%M:%S")
print "DS1307 =\t%s" % now
