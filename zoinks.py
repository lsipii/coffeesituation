#!/usr/bin/env python3
"""
@author lsipii
"""
import sys, getopt
from flask import Flask
from controllers.Zoinks import Zoinks

# Creates the flask app
app = Flask(__name__)
# App controller
controller = Zoinks()

# Defines the app routes
@app.route('/', methods=controller.knownHttpMethods)
@app.route('/<path>', methods=controller.knownHttpMethods)
def request():
	return controller.getZoinkResponse()

# App runner
if __name__ == '__main__':

	argv = sys.argv[1:]
	
	# Sets the app debug mode
	debugMode = True

	# Help texts
	def printHelp():
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
			print("v1")
			exit()
		if opt in ("-p", "--production"):
			debugMode = False

	# Run app
	controller.setDebugMode(debugMode)
	app.run(debug=debugMode)
