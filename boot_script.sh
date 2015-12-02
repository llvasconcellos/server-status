#!/bin/sh

cd /home/root/gpio

# mount SD before anything else
mount /dev/mmcblk1p1 /home/root/debian/home/buendia/sd/

# SERVER STATUS
python server_status.py >> sd/server_status_log.txt 2>&1 &

# BATTERY STATUS
echo 101 > battery_charge.txt  # reset status file
python battery_status.py >> sd/battery_status_log.txt 2>&1 &
# sleep briefly to allow default UART pin boot sequence to finish (a bug workaround)
( sleep 15 ; python battery_led.py >> sd/battery_led_log.txt 2>&1) &

# OTHER SCRIPTS
# log battery charge history
. log_charge.sh &

# truncate log files
. truncate_logs.sh &

# truncate battery log
truncate() { tail -$2 $1 > $1.tmp; cat $1.tmp > $1; rm $1.tmp; }
truncate sd/battery_charge_log.tmp 1000

exit 0
