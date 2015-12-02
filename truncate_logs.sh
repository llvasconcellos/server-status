#!/bin/sh

# Every 3 hours truncate the 3 main log files on SD card to 1000 lines

cd /home/root/gpio/sd

echo "system reboot" >> battery_led_log.txt
echo "system reboot" >> battery_status_log.txt
echo "system reboot" >> server_status_log.txt
echo "system reboot" >> battery_charge_log.txt

truncate() { tail -$2 $1 > $1.tmp; cat $1.tmp > $1; rm $1.tmp; }

while true; do
truncate battery_led_log.txt 1000
truncate battery_status_log.txt 1000
truncate server_status_log.txt 1000
sleep 10800
done
