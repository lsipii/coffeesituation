#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import request
from flask_responses import json_response

class BaseController():

	"""
	Base controller module initialization
	@var (array) knownHttpMethods
	"""
	knownHttpMethods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def get(self, path = None):
		return self.getNotFoundResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def head(self, path = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def put(self, path = None):
		return self.getMethodNotSupportedResponse()
	def set(self, path = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def delete(self, path = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def connect(self, path = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def options(self, path = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def trace(self, path = None):
		return self.getMethodNotSupportedResponse()

	"""
	The base request handler
	
	@params (string) path = None
	@return (json_response)
	"""
	def patch(self, path = None):
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
	@param (int) responseCode
	@return (json_response)
	"""
	def getErrorResponse(self, message = None, responseCode = 500):
		if message is None:
			message = "App setup error"
		return self.getJsonResponse({"message": message}, responseCode)

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
	Gets the request method
	
	@return (string) method
	"""
	def getRequestMethod(self):
		return request.method

	"""
	Gets the request params
	
	@return (dict) params
	"""
	def getRequestParams(self):

		if self.getRequestMethod() == 'POST':
			return request.form.to_dict()
		elif self.getRequestMethod() == 'GET':
			return request.args.to_dict()
		else:
			return {}
