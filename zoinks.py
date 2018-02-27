#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import Flask
from controllers.Zoinks import Zoinks

# Sets the app debug mode
debugMode = False

# Creates the flask app
app = Flask(__name__)
# App controller
controller = Zoinks(debugMode)

# Defines the app routes
@app.route('/', methods=controller.knownHttpMethods)
def request():
	return controller.getZoinkResponse()

if __name__ == '__main__':
    app.run(debug=debugMode)