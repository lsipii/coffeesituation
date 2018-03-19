#!/usr/bin/env bash
# @author lsipii
#  
# Example crontask, once in hour:
# 57 * * * * ensureSlackBotAppRunning.sh

# ensure running in project root folder
cd "${0%/*}/.."

if ps x | grep -v grep | grep -q slackbotApp.py
then
    echo "SlackBotApp.py is running"
else
	echo "SlackBotApp.py was not running, engage.."
    ./slackbotApp.py --production &
fi