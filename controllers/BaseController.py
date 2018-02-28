#!/usr/bin/env python3
"""
@author lsipii
"""
from flask_responses import json_response

class BaseController():

	"""
	Constructor
	"""
	def __init__(self):
		"""
		List of shell apps that we require

		@var (array) shellApplicationRequirements
		"""
		self.shellApplicationRequirements = []


	"""
	Base controller module initialization
	@var (array) knownHttpMethods
	"""
	knownHttpMethods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def get(self, params = None):
		return self.getNotFoundResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def head(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def put(self, params = None):
		return self.getMethodNotSupportedResponse()
	def set(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def delete(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def connect(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def options(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def trace(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (dict) params = None
	@return (json_response)
	"""
	def patch(self, params = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request method not supported response
	
	@params (dict) params = None
	@return (json_response)
	"""
	def getMethodNotSupportedResponse(self, params = None):
		return self.getJsonResponse({"message": "Why are you jamming?"}, 405)

	"""
	The base 404 response
	
	@params (dict) params = None
	@return (json_response)
	"""
	def getNotFoundResponse(self, params = None):
		return self.getJsonResponse({"message": "Why are you jamming?"}, 404)

	"""
	The base 401 response
	
	@params (dict) params = None
	@return (json_response)
	"""
	def getAccessDeniedResponse(self, params = None):
		return self.getJsonResponse({"message": "Why are you jamming?"}, 401)

	"""
	The base 500 response
	
	@param (mixed) message
	@return (json_response)
	"""
	def getErrorResponse(self, message = None):
		if message is None:
			message = "App setup error"
		return self.getJsonResponse({"message": message}, 500)

	"""
	The a json response
	
	@param (mixed) response = None
	@param (int) responseCode = 200
	@return (json string)
	"""
	def getJsonResponse(self, response = None, responseCode = 200):
		if response is None:
			response = {"message": "Undefined error"}
		return json_response(response, status_code=responseCode)


	"""
	Sets the list of shell apps that we require
	"""
	def setRequiredShellApps(self, listOfShellAppNames):
		self.shellApplicationRequirements = listOfShellAppNames

	"""
	Validate controller
	"""
	def validateControllersFunctionality(self):

		from utils.Utils import validateAppRequirements

		for shellApp in self.shellApplicationRequirements:
			validateAppRequirements(shellApp) # Exits
