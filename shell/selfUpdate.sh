#!/usr/bin/env bash
# @author lsipii
#  
# Example crontask, once in a day:
# 15 2 * * * selfUpdate.sh

# Ensure running in project root folder
cd "${0%/*}/.."

# Fetch remote
git fetch
if [ ! $(git rev-parse HEAD) == $(git rev-parse @{u}) ];then
	echo "Updating to the latest.."
    git reset --hard HEAD
    git pull
    
    # Restart slackbot app if running
    if ps x | grep -v grep | grep -q slackbotApp.py
   	then
   		kill $(pgrep -f 'slackbotApp.py')
   		./shell/ensureSlackBotAppRunning.sh
   	fi

   	# Restart the device app if running
   	if ps x | grep -v grep | grep -q deviceApp.py
   	then
   		kill $(pgrep -f 'deviceApp.py')
   		./shell/ensureDeviceAppRunning.sh
   	fi
fi