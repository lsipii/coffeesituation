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
	def __init__(self, debugMode):	
		self.accessChecker = AccessChecker(debugMode)
		
	"""
	Basic a very much of a intresting response, or maybe something different

	@return (BaseController response)
	"""
	def getZoinkResponse(self):
		if self.accessChecker.ifAccessGranted():
			try:
				coffeeChecker = CoffeeChecker()
				return coffeeChecker.hasWeCoffee()
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
