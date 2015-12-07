#!/bin/sh

# runs in background to assess if LED scripts are working properly
# creates/kills instances of report_failed_process.py to report failures

cd /home/root/gpio

while true; do
	prs=$(ps)

	# have any LED scripts failed?
	batt=$(echo "$prs" | grep battery_status.py | grep -v grep | wc -l);
	serv=$(echo "$prs" | grep server_status.py | grep -v grep | wc -l)

	# are any fail-report scripts active?
	failbatt=$(echo "$prs" | grep "report_failed_process.py battery" | grep -v grep | wc -l);
	failserv=$(echo "$prs" | grep "report_failed_process.py server" | grep -v grep | wc -l);

	# report failures to LED if new
	[ $batt != 1 ] && [ $failbatt == 0 ] && python report_failed_process.py battery &
	[ $serv != 1 ] && [ $failserv == 0 ] && python report_failed_process.py server & 

	# kill any script-failed processes that are no longer correct
	[ $failbatt -gt 0 ] && [ $batt == 1 ] && kill $(echo "$prs" | grep 'report_failed_process.py battery' | grep -v grep | grep -oE '[0-9]+' | head -n 1)
	[ $failserv -gt 0 ] && [ $serv == 1 ] && kill $(echo "$prs" | grep 'report_failed_process.py server' | grep -v grep | grep -oE '[0-9]+' | head -n 1)

	# log new script failures
	[ $batt != 1 ] && [ $failbatt == 0 ] && printf "battery_status.py "$batt" instance(s)\\n" >> sd/battery_status_log.txt
	[ $serv != 1 ] && [ $failserv == 0 ] && printf "server_status.py "$serv" instance(s)\\n" >> sd/server_status_log.txt

	sleep 15
done
