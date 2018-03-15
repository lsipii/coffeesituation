#!/usr/bin/env python3
"""
@author lsipii
"""
import sys, getopt
from app.ConfigReader import ConfigReader
from app.slack.SlackBot import SlackBot

# App runner
if __name__ == '__main__':

	argv = sys.argv[1:]
	
	# Sets the app debug mode
	debugMode = True

	# Help texts
	def printHelp():
		print("Usage: bot.py --help|--version") 
		exit()
		
	try:
		opts, args = getopt.getopt(argv, "hvp", ["help", "version"])
	except getopt.GetoptError:
		printHelp()

	for opt, arg in opts:

		if opt in ("-h", "--help"):
			printHelp()
		if opt in ("-v", "--version"):
			print("v1")
			exit()
		if opt in ("-p", "--production"):
			debugMode = False

	# Run the bot
	config = ConfigReader("slackbot").getConfig()
	bot = SlackBot(config)
	bot.setDebugMode(debugMode)
	bot.engage()
