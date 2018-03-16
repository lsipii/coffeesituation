#!/usr/bin/env python3
"""
@author lsipii
"""
import sys, getopt
from slackbot.SlackBotApp import SlackBotApp
from slackbot.SlackBot import SlackBot

# App runner
if __name__ == '__main__':

	argv = sys.argv[1:]
	
	# Sets the app debug mode
	debugMode = True

	# Bot app infos
	app = SlackBotApp()
	
	# Help texts
	def printHelp():
		print(app.getFullAppName())
		print("Mission statement: "+ app.getAppMissionStatement(), "\n")
		print("Usage: slackbot.py --help|--version|--production") 
		exit()
		
	try:
		opts, args = getopt.getopt(argv, "hvp", ["help", "version", "production"])
	except getopt.GetoptError:
		printHelp()

	for opt, arg in opts:

		if opt in ("-h", "--help"):
			printHelp()
		if opt in ("-v", "--version"):
			print(app.getFullAppName())
			exit()
		if opt in ("-p", "--production"):
			debugMode = False

	# Run the bot
	bot = SlackBot(app)
	bot.setDebugMode(debugMode)
	bot.engage()
