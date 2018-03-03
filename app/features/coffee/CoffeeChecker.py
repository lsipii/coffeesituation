#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.coffee.CoffeeActionAccessChecker import CoffeeActionAccessChecker
from app.features.CameraShooter import CameraShooter
from app.features.CameraStreamer import CameraStreamer
from app.hardware.MediaStorage import MediaStorage

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs [storage]
	"""
	def __init__(self, configs):
		self.storage = MediaStorage(configs["storage"])
		self.cameraShooter = CameraShooter(self.storage)
		self.cameraStreamer = CameraStreamer(configs["app"])
		self.coffeeActionAccessChecker = CoffeeActionAccessChecker(configs["coffeeAccess"])

	"""
	Checks if we have coffe
	
	@param (dict) requestParams = None
	@return (dict) {
		(string) hasCoffee
		(string) coffeeObservationImageUrl
	}
	"""
	def hasWeCoffee(self, requestParams = None):

		# Check for mode change requests
		self.checkForModeChangeRequests(requestParams)

		# Get coffee data from selected service
		if self.cameraStreamer.areWeCurrentlyStreaming():
			coffeeObservationUrl = self.cameraStreamer.getStreamUrl()
		else:
			self.cameraShooter.takeAPhoto() 
			coffeeObservationUrl = self.cameraShooter.getPhotoStorageUrl()
				
		return {
			"hasCoffee": "dunno", # To be implemented, opencv etc
			"coffeeObservationUrl": coffeeObservationUrl,
			"streaming": self.cameraStreamer.areWeCurrentlyStreaming(),
		}

	"""
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		apps = CameraShooter.shellApplicationRequirements + CameraStreamer.shellApplicationRequirements
		return apps

	"""
	Checks if we have a coffee MODE change and executes it
	
	@param (dict) requestParams = None
	@return (dict) accessGrantedToCommandAction, {command, action}
	"""
	def checkForModeChangeRequests(self, requestParams = None):

		grantedAction = self.coffeeActionAccessChecker.getRequestedAndAllowedCommandAction(requestParams)
		if grantedAction["command"] is not None:
			if grantedAction["command"] == "stream":
				if grantedAction["action"] == "ON": 
					self.cameraStreamer.startStreaming()
				elif grantedAction["action"] == "OFF":
					self.cameraStreamer.stopStreaming()