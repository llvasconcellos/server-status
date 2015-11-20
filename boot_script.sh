#!/bin/sh

# mount SD before anything else
mount /dev/mmcblk1p1 /home/root/debian/home/buendia/sd/

# SERVER STATUS

# python /home/root/gpio/server_status.py >> /home/root/gpio/sd/server_status_log.txt 2>&1 &

# BATTERY STATUS

# echo 101 > /home/root/gpio/battery_charge.txt  # reset status file

# python /home/root/gpio/battery_status.py >> /home/root/gpio/sd/battery_status_log.txt 2>&1 &

# sleep briefly to allow default UART pin boot sequence to finish (a bug workaround)
# ( sleep 15 ; python /home/root/gpio/battery_led.py >> /home/root/gpio/sd/battery_led_log.txt 2>&1) &
