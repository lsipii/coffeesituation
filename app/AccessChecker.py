#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import request

class AccessChecker():

	"""
	Module initialization

	@param (dict) accessConfig
	@param (bool) debugMode
	""" 
	def __init__(self, accessConfig, debugMode = False):
		self.accessConfig = accessConfig
		self.debugMode = debugMode
		self.accessKeyParamKeyName = "api_token"

	"""
	Checks the request for correct credential details, passed as request params 

	@param (dict) requestParams, [app, api_token]
	@param (string) requestMethod
	@return (bool) accessGranted
	"""
	def ifAccessGranted(self, requestParams, requestMethod):

		accessGranted = False

		if self.accessKeyParamKeyName in requestParams:
			if "app" in requestParams and requestParams["app"] in self.accessConfig:
				if self.debugMode and requestMethod == "GET":
					accessGranted = self.getAccessDetailsFromTheRequest(requestParams)
				elif requestMethod == "POST":
					accessGranted = self.getAccessDetailsFromTheRequest(requestParams)

		return accessGranted

	"""
	Checks the request has access params by get method
	
	@param (dict) requestParams, [app, api_token]
	@return (bool) hasCorrectAccessParams
	"""
	def getAccessDetailsFromTheRequest(self, requestParams):
		if self.accessConfig[requestParams["app"]][self.accessKeyParamKeyName] == requestParams[self.accessKeyParamKeyName]:
			return True
		return False

	"""
	Sets debug mode
	
	@param (bool) debugMode
	"""
	def setDebugMode(self, debugMode):
		self.debugMode = debugMode
