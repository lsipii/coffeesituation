#!/usr/bin/env bash
# @author lsipii
#  
# Example crontask, once in hour:
# 10 * * * * ensureRaspberryPiNetwork.sh

# Ping google, restart interfaces on a connection error
ping -c2 google.com > /dev/null
if [ $? != 0 ]; then
	echo "Restarting network connection.."
	sudo ifdown wlan0
	sudo ifup wlan0
fi