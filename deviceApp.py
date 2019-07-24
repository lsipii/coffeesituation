#!/usr/bin/env python3
"""
@author lsipii
"""
import sys, getopt
from flask import Flask
from apps.DeviceApp.DeviceApp import DeviceApp
from apps.DeviceApp.http.controllers.CoffeesHasWeController import CoffeesHasWeController

# Creates the device app
app = DeviceApp()
# Creates the flask router app
routerApp = Flask(__name__)
# The app controller
controller = CoffeesHasWeController(app)

# Defines the app routes
@routerApp.route('/', methods=controller.knownHttpMethods)
@routerApp.route('/<path>', methods=controller.knownHttpMethods)
def request(path = None):
	return controller.getCoffeeResponse(path)

# App runner
if __name__ == '__main__':

	argv = sys.argv[1:]
	
	# Sets the app debug mode
	debugMode = True

	# Help texts
	def printHelp():
		print(app.getFullAppName())
		print("Mission statement: "+ app.getAppMissionStatement(), "\n")
		print("Usage: zoinks.py --help|--version|--production") 
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

	# Run app
	controller.setDebugMode(debugMode)
	controller.validateZoinksFunctionality()
	routerApp.run(debug=debugMode)
