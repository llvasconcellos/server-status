#!/usr/bin/env python

# This script sets the time on the RTC.  It should only be run when Yocto is connected
# to the internet and it's system time is correct
# 30s is added to prevent any web-connected tablet from creeping slightly ahead

import SDL_DS1307
from datetime import timedelta

ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)
#ds1307.write_now()

time_now = datetime.now()
add30s = timedelta(0, 30)
set_time = time_now + add30s

ds1307.write_datetime(set_time)
