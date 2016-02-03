#!/bin/sh

# Runs in background to assess if server/battery status reporting scripts are working properly

cd /home/root/gpio

while true; do
	prs=$(ps)
	echo $(date)

	# filter relevant process rows
	batt_lines=$(echo "$prs" | grep battery_status.py | grep -v grep);
	serv_lines=$(echo "$prs" | grep server_status.py | grep -v grep);
	butt_lines=$(echo "$prs" | grep button_shutdown.py | grep -v grep);
	
	# Have any scripts failed? These lines count process lines
	batt=$(echo "$batt_lines" | sed '/^\s*$/d' | wc -l);  # sed to ignore empty lines
	serv=$(echo "$serv_lines" | sed '/^\s*$/d' | wc -l);
	butt=$(echo "$butt_lines" | sed '/^\s*$/d' | wc -l);

	# actions to take
	[ $batt == 0 ] && echo 'battery_status.py failed'
	[ $serv == 0 ] && echo 'server_status.py failed' && python /home/root/gpio/lcd/report_lines_and_battery.py 'Server info not' 'reporting.' &
	[ $butt == 0 ] && echo 'button_shutdown.py failed' && python button_shutdown.py >> sd/logs/button_log.txt 2>&1 &
	sleep 60
done
