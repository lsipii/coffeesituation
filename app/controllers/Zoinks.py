#!/usr/bin/env python3
"""
@author lsipii
"""
from app.AccessChecker import AccessChecker
from app.ConfigReader import ConfigReader
from app.controllers.BaseController import BaseController
from app.features.CoffeeChecker import CoffeeChecker
from app.utils.Utils import validateAppRequirements
from app.utils.Slack import Slack

class Zoinks(BaseController):

	"""
	Zoinks module initialization
	
	@param (bool) debugMode
	"""
	def __init__(self, debugMode = False):
		self.debugMode = debugMode

		self.config = ConfigReader().getConfig()		
		self.accessChecker = AccessChecker(self.debugMode)
		self.coffeeChecker = CoffeeChecker(self.config["storage"])
		self.notifier = Slack(self.config["slack"])

		self.validateZoinksFunctionality()
		
	"""
	Basic a very much of a intresting response, or maybe something different
	
	@param (string) path = None
	@return (BaseController response)
	"""
	def getZoinkResponse(self, path = None):
		if self.accessChecker.ifAccessGranted():
			try:
				coffeeResponse = self.coffeeChecker.hasWeCoffee()
				if "slackNotice" in coffeeResponse:
					self.notifier.send(coffeeResponse["slackNotice"])
				return self.getJsonResponse(coffeeResponse)
			except Exception as e:
				if self.accessChecker.debugMode:
					return self.getErrorResponse(str(e))
				else:
					return self.getErrorResponse()
		else:
			return self.getAccessDeniedResponse()

	"""
	Zoinks module accepted http methods
	
	@param (array) acceptedHttpMethods
	"""
	def getAccpetedMethods(self):	
		return self.acceptedHttpMethods;

	"""
	Sets debug mode
	
	@param (bool) debugMode
	"""
	def setDebugMode(self, debugMode):
		self.debugMode = debugMode
		self.accessChecker.setDebugMode(self.debugMode)

	"""
	Validate app runtime
	"""
	def validateZoinksFunctionality(self):

		for shellApp in self.coffeeChecker.getRequiredShellApps():
			validateAppRequirements(shellApp) # Throws

		self.coffeeChecker.storage.validateStorageFunctionality() # Throws

