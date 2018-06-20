#!/usr/bin/env bash
# @author lsipii
#  
# Example crontask, once in hour:
# */20 * * * * ensureRaspberryPiNetwork.sh

# Ping google, restart interfaces on a connection error
ping -c2 8.8.8.8 > /dev/null
if [ $? != 0 ]; then
	echo "Restarting network connection.."
	sudo ifdown --force wlan0
	sudo ifup wlan0
	sleep 10
	sudo ifup wlan0
elif ! ps -ef | grep dataplicity | grep python > /dev/null;then
	echo "Restarting the tuxtunnel.."
	sudo supervisorctl restart tuxtunnel
fi