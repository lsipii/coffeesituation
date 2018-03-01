#!/usr/bin/env python3
"""
@author lsipii
"""
from app.AccessChecker import AccessChecker
from app.ConfigReader import ConfigReader
from app.controllers.BaseController import BaseController
from app.features.CoffeeChecker import CoffeeChecker
from app.features.CoffeeToSlacker import CoffeeToSlacker
from app.utils.Utils import validateAppRequirements

class CoffeesHasWeController(BaseController):

	"""
	Zoinks module initialization
	
	@param (bool) debugMode
	"""
	def __init__(self, debugMode = False):
		self.debugMode = debugMode

		self.config = ConfigReader().getConfig()		
		self.accessChecker = AccessChecker(self.debugMode)
		self.coffeeChecker = CoffeeChecker(self.config["storage"])
		self.notifier = CoffeeToSlacker(self.config["slack"])

		self.validateZoinksFunctionality()
		
	"""
	Basic a very much of a intresting response, or maybe something different
	
	@param (string) path = None
	@return (BaseController response)
	"""
	def getCoffeeResponse(self, path = None):
		if self.accessChecker.ifAccessGranted():
			try:
				coffeeResponse = self.coffeeChecker.hasWeCoffee()

				# If a new image was taken, report to slack channels
				if coffeeResponse["newObservationFappened"]:
					self.notifier.notify(coffeeResponse)

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

