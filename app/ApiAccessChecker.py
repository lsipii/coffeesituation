#!/usr/bin/env python3
"""
@author lsipii
"""
from flask import request
from datetime import datetime
from app.http.exceptions.RequestException import RequestException

class ApiAccessChecker():

	"""
	Module initialization

	@param (dict) accessConfig
	@param (bool) debugMode
	""" 
	def __init__(self, accessConfig, debugMode = False):
		self.accessConfig = accessConfig
		self.debugMode = debugMode
		self.accessKeyParamKeyName = "api_token"

		self.requestTimes = {
			"current": None,
			"previous": None,
			"channels": {}
		}

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

	"""
	Throttle request
	
	@param (string) requestMethod = "GET"
	@param (dict) requestParams = None
	"""
	def throttleRequest(self, requestMethod  = "GET", requestParams = None):

		if requestMethod is "GET" or (requestParams is None or "channel" not in requestParams):
			self.throttleRequestByTimesContainer(self.requestTimes, 1) # throws
		else:
			channel = requestParams["channel"]
			
			# Init the channel times container
			if channel not in self.requestTimes["channels"]:
				self.requestTimes["channels"][channel] = {
					"current": None,
					"previous": None
				}

			self.throttleRequestByTimesContainer(self.requestTimes["channels"][channel], 5) # throws

	"""
	Throttle request
	
	@param (dict) timesContaier
	@param (int) throttleLimit, in seconds
	"""
	def throttleRequestByTimesContainer(self, timesContaier, throttleLimit):

		timesContaier["current"] = datetime.now()
		if timesContaier["previous"] is None:
			timesContaier["previous"] = datetime.now()

		# Calc the secs
		difference = timesContaier["current"] - timesContaier["previous"]  #  Note: returns timedelta obj
		secondsDifference = int(difference.total_seconds())
		if secondsDifference < 0:
			secondsDifference = 0

		# Store for the next request
		timesContaier["previous"] = datetime.now()

		# If initial or below the throttling limit
		if secondsDifference != 0 and secondsDifference <= throttleLimit:
			raise RequestException("Too many request on too little amount of time", 429)
