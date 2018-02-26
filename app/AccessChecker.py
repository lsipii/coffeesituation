#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import request
from flask import current_app as app

class AccessChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.accessKeyParamKeyName = "accessKey"
		self.accessKey = "kyllig"

	"""
	Checks the request for correct credential details, passed as request params 
	
	@return (bool) accessGranted
	"""
	def ifAccessGranted(self):

		requestAccessKey = None

		if app.debug and self.requestHasAccessKeyByGetRequest():
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
		if app.debug and request.method == 'GET':
			param = self.getAccessKeyFromGetRequest()
			return param is not None
		return False

	"""
	Checks the request has access params by get method
	
	@return (bool) hasCorrectAccessParams
	"""
	def requestHasAccessKeyByPostRequest(self):
		if request.method == 'POST':
			param = self.getAccessKeyFromPostRequest()
			return param is not None
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
		return request.json.get(self.accessKeyParamKeyName)

