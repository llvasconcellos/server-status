#!/bin/sh

# Every 10 minutes log battery level

cd /home/root/gpio

while true; do

cp battery_charge.txt sd/battery_charge.txt
cat battery_charge.txt >> sd/battery_charge_log.txt

sleep 600
done
