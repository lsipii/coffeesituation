#!/usr/bin/env python3
"""
@author lsipii
"""
from app.AccessChecker import AccessChecker
from controllers.BaseController import BaseController
from features.CoffeeChecker import CoffeeChecker

class Zoinks(BaseController):

	"""
	Zoinks module initialization
	
	@param (bool) debugMode
	"""
	def __init__(self, debugMode = False):
		self.debugMode = debugMode
		self.coffeeChecker = CoffeeChecker()
		self.accessChecker = AccessChecker(self.debugMode)
		self.validateZoinksFunctionality()
		
	"""
	Basic a very much of a intresting response, or maybe something different

	@return (BaseController response)
	"""
	def getZoinkResponse(self):
		if self.accessChecker.ifAccessGranted():
			try:
				coffeeResponse = self.coffeeChecker.hasWeCoffee()
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

		from utils.Utils import validateAppRequirements
		for shellApp in self.coffeeChecker.getRequiredShellApps():
			validateAppRequirements(shellApp) # Throws

		self.coffeeChecker.storage.validateStorageFunctionality() # Throws

