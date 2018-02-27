#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import request

class AccessChecker():

	"""
	Module initialization
	"""
	def __init__(self, debugMode):
		self.debugMode = debugMode
		self.accessKeyParamKeyName = "accessKey"
		self.accessKey = "kyllig"

	"""
	Checks the request for correct credential details, passed as request params 
	
	@return (bool) accessGranted
	"""
	def ifAccessGranted(self):

		requestAccessKey = None

		if self.debugMode and self.requestHasAccessKeyByGetRequest():
			requestAccessKey = self.getAccessKeyFromGetRequest()
		elif self.requestHasAccessKeyByPostRequest():
			requestAccessKey = self.getAccessKeyFromPostRequest()

		if requestAccessKey == self.accessKey:
			return True
		return False

	"""
	Checks the request has access params by get method
	
	@return (bool) hasCorrectAccessParams
	"""
	def requestHasAccessKeyByGetRequest(self):
		if self.debugMode and request.method == 'GET':
			param = self.getAccessKeyFromGetRequest()
			return param is not None
		return False

	"""
	Checks the request has access params by get method
	
	@return (bool) hasCorrectAccessParams
	"""
	def requestHasAccessKeyByPostRequest(self):
		if request.method == 'POST' and self.accessKeyParamKeyName in request.form:
			return True
		return False

	"""
	Gets the access key from a get param
	
	@return (string|None) accessKey
	"""
	def getAccessKeyFromGetRequest(self):
		return request.args.get(self.accessKeyParamKeyName)

	"""
	Gets the access key from a get param
	
	@return (string|None) accessKey
	"""
	def getAccessKeyFromPostRequest(self):
		return request.form[self.accessKeyParamKeyName]
