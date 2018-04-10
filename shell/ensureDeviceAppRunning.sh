#!/usr/bin/env bash
# @author lsipii
#  
# Example crontask, once in hour:
# 20 * * * * ensureDeviceAppRunning.sh

# ensure running in project root folder
cd "${0%/*}/.."

if ps x | grep -v grep | grep -q deviceApp.py
then
    echo "deviceApp.py is running"
else
	echo "deviceApp.py was not running, engage.."
    ./deviceApp.py --production &
fi