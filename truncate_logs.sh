#!/bin/sh

# Every 6 hours truncate the main log files on SD card to 5000 lines

cd /home/root/gpio/sd

echo "system reboot" >> battery_status_log.txt
echo "system reboot" >> server_status_log.txt

truncate() { tail -$2 $1 > $1.tmp; cat $1.tmp > $1; rm $1.tmp; }

while true; do
	truncate battery_status_log.txt 5000
	truncate server_status_log.txt 5000
	sleep 21600
done
