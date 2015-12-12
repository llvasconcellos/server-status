#!/bin/sh

# Runs in background to assess if LED scripts are working properly
# Creates/kills instances of report_failed_process.py to report failures

cd /home/root/gpio

while true; do
	prs=$(ps)

	# filter relevant process rows
	batt_lines=$(echo "$prs" | grep battery_status.py | grep -v grep);
	serv_lines=$(echo "$prs" | grep server_status.py | grep -v grep);
	
	# Have any LED scripts failed? These lines count process lines, returning '1' if ok and '0' otherwise
	batt=$(echo "$batt_lines" | wc -l);
	serv=$(echo "$serv_lines" | wc -l);

	# Are any failed-script report scripts active?
	failbatt=$(echo "$prs" | grep "report_failed_process.py battery" | grep -v grep | wc -l);
	failserv=$(echo "$prs" | grep "report_failed_process.py server" | grep -v grep | wc -l);

	# Report failures to LED if new
	[ $batt != 1 ] && [ $failbatt == 0 ] && python report_failed_process.py battery &
	[ $serv != 1 ] && [ $failserv == 0 ] && python report_failed_process.py server & 

	# Kill any script-failed processes that are no longer correct
	[ $failbatt == 1 ] && [ $batt == 1 ] && kill $(echo "$prs" | grep 'report_failed_process.py battery' | grep -v grep | grep -oE '[0-9]+' | head -n 1)
	[ $failserv == 1 ] && [ $serv == 1 ] && kill $(echo "$prs" | grep 'report_failed_process.py server' | grep -v grep | grep -oE '[0-9]+' | head -n 1)

	# Log new script failures
	[ $batt != 1 ] && [ $failbatt == 0 ] && printf "battery_status.py "$batt" instance(s)\\n" >> sd/battery_status_log.txt
	[ $serv != 1 ] && [ $failserv == 0 ] && printf "server_status.py "$serv" instance(s)\\n" >> sd/server_status_log.txt

	# kill excess script instances
	[ $batt -gt 1 ] && for i in $(seq $(expr $batt - 1)); do kill $(echo "$batt_lines" | sed -n $i'p' | grep -oE '[0-9]+' | head -n 1); done && echo duplicate process killed >> sd/battery_status_log.txt
	[ $serv -gt 1 ] && for i in $(seq $(expr $serv - 1)); do kill $(echo "$serv_lines" | sed -n $i'p' | grep -oE '[0-9]+' | head -n 1); done && echo duplicate process killed >> sd/server_status_log.txt
	
	sleep 15
done

