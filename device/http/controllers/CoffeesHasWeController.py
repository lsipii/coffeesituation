#!/usr/bin/env python3
"""
@author lsipii
"""
from device.http.controllers.BaseController import BaseController
from device.http.exceptions.RequestException import RequestException
from device.ApiAccessChecker import ApiAccessChecker
from device.features.coffee.CoffeeChecker import CoffeeChecker
from device.features.coffee.CoffeeToSlacker import CoffeeToSlacker
from app.utils.Utils import validateAppRequirements

class CoffeesHasWeController(BaseController):

	"""
	Zoinks module initialization
	
	@param (AppInfo) app
	"""
	def __init__(self, app):
		
		# References
		self.app = app
		self.config = self.app.config		
		self.accessChecker = ApiAccessChecker(self.config["apiAccess"])
		self.coffeeChecker = CoffeeChecker(self.config)
		self.notifier = CoffeeToSlacker(self.config["slack"])

		# Internal states
		self.debugMode = False
		
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
				if self.debugMode:
					if path is None:
						print("Accessing a root path")
					else:
						print("Accessing a path: "+path)

				if path is None:
					return self.getCoffeeSituationResponse(requestMethod, requestParams)
				elif path == "status":
					return self.getCoffeeAppStatusReponse()
				else:
					return self.getNotFoundResponse()
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
	@return (BaseController response) {coffee, notify}
	"""
	def getCoffeeSituationResponse(self, requestMethod, requestParams):

		coffeeResponse = self.coffeeChecker.hasWeCoffee(requestParams)
		notifyResponse = self.notifier.generateResponsePayload(coffeeResponse, requestParams)

		if self.config["app"]["settings"]["sendSlackNotifications"]: 
			if self.debugMode:
				print("Sending slack notification..")
			try:
				self.notifier.notify(notifyResponse)
				notifyResponse["sent"] = True
			except Exception as e:
				notifyResponse["sent"] = False

		return self.getJsonResponse({
			"coffee": coffeeResponse,
			"notify": notifyResponse
		})

	"""
	Basic a very much of a intresting response, or maybe something different
	
	@param (string) path = None
	@return (BaseController response) {status, streaming}
	"""
	def getCoffeeAppStatusReponse(self):
		return self.getJsonResponse({
			"status": "OK",
			"streaming": self.coffeeChecker.areWeCurrentlyStreaming()
		})

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
		self.coffeeChecker.setDebugMode(self.debugMode)

	"""
	Validate app runtime
	"""
	def validateZoinksFunctionality(self):

		shellApps = self.coffeeChecker.getRequiredShellApps()
		for shellApp in shellApps:
			try:
				validateAppRequirements(shellApp.shellApplicationRequirements) # Throws
			except Exception as e:
				if self.debugMode:
					shellApp.shellApplicationRequirementsMet = False
					print(e) # Keep running, accept resulting exceptions
				else:
					raise e

		try:
			self.coffeeChecker.storage.validateStorageFunctionality() # Throws
		except Exception as e:
				if self.debugMode:
					print(e) # Keep running, accept resulting exceptions
				else:
					raise e