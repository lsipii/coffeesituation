#!/usr/bin/env bash
# @author lsipii
#  
# Example crontask, once in hour:
# 10 * * * * ensureRaspberryPiNetwork.sh

# Ping google, restart interfaces on a connection error
ping -c2 8.8.8.8 > /dev/null
if [ $? != 0 ]; then
	echo "Restarting network connection.. by rebooting!"
	sudo reboot
fi