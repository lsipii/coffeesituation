#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.CoffeeQueryModeControl import CoffeeQueryModeControl
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
		self.modeControl = CoffeeQueryModeControl(self)

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
		self.modeControl.checkForModeChangeRequests(requestParams)

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