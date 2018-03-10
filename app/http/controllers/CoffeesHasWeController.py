#!/usr/bin/env python3
"""
@author lsipii
"""
from app.http.controllers.BaseController import BaseController
from app.http.exceptions.RequestException import RequestException
from app.ApiAccessChecker import ApiAccessChecker
from app.ConfigReader import ConfigReader
from app.features.coffee.CoffeeChecker import CoffeeChecker
from app.features.coffee.CoffeeToSlacker import CoffeeToSlacker
from app.utils.Utils import validateAppRequirements

class CoffeesHasWeController(BaseController):

	"""
	Zoinks module initialization
	
	@param (bool) debugMode
	"""
	def __init__(self, debugMode = False):
		self.debugMode = debugMode

		self.config = ConfigReader().getConfig()		
		self.accessChecker = ApiAccessChecker(self.config["apiAccess"], self.debugMode)
		self.coffeeChecker = CoffeeChecker(self.config)
		self.notifier = CoffeeToSlacker(self.config["slack"])
		
	"""
	Basic a very much of a intresting response, or maybe something different
	
	@param (string) path = None
	@return (BaseController response)
	"""
	def getCoffeeResponse(self, path = None):

		requestMethod=self.getRequestMethod()
		requestParams=self.getRequestParams()

		try:
			self.accessChecker.throttleRequest(requestMethod, requestParams) # throws
			if self.accessChecker.ifAccessGranted(requestParams, requestMethod):
				coffeeResponse = self.coffeeChecker.hasWeCoffee(requestParams) 
				#self.notifier.notifyCoffeeRequest(coffeeResponse, requestParams)
				return self.getJsonResponse(coffeeResponse)
			else:
				return self.getAccessDeniedResponse()
		except RequestException as e:
			return self.getErrorResponse(e.message, e.code)
		except Exception as e:
			if self.debugMode:
				return self.getErrorResponse(str(e))
			else:
				return self.getErrorResponse()

	"""
	Basic a very much of a intresting response, or maybe something different
	
	@param (string) path = None
	@return (BaseController response)
	"""
	def getSomeResponse(self, path = None):

		requestMethod=self.getRequestMethod()
		requestParams=self.getRequestParams()

		try:
			self.accessChecker.throttleRequest(requestMethod, requestParams) # throws
		except RequestException as e:
			return self.getErrorResponse(e.message, e.code)
		return self.getNotFoundResponse()
				

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

		try:
			shellApps = self.coffeeChecker.getRequiredShellApps()
			for shellApp in shellApps:
				validateAppRequirements(shellApp) # Throws

			self.coffeeChecker.storage.validateStorageFunctionality() # Throws
		except Exception as e:
			if self.debugMode:
				print(e) # Keep running, accept resulting exceptions
			else:
				raise e