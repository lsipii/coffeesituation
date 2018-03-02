#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.CameraShooter import CameraShooter
from app.features.CameraStreamer import CameraStreamer
from app.hardware.MediaStorage import MediaStorage

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs [storage]
	"""
	def __init__(self, configs):
		self.storage = MediaStorage(configs)
		self.cameraShooter = CameraShooter(self.storage)
		self.cameraStreamer = CameraStreamer(configs)

	"""
	Checks if we have coffe
	
	@param (dict) requestParams = None
	@return (dict) {
		(string) hasCoffee
		(string) coffeeObservationImageUrl
		(bool) newObservationFappened
	}
	"""
	def hasWeCoffee(self, requestParams = None):

		# Check for mode change requests
		self.checkForModeChangeRequests(requestParams)

		# Get coffee data from selected service
		if self.cameraStreamer.areWeCurrentlyStreaming():
			newObservationFappened = True
			coffeeObservationUrl = self.cameraStreamer.getStreamUrl()
		else:
			newObservationFappened = False
			if self.shouldWeTakeAPhoto(): 
				self.cameraShooter.takeAPhoto() 
				newObservationFappened = True
				
			coffeeObservationUrl = self.cameraShooter.getPhotoStorageUrl()
				
		return {
			"hasCoffee": "dunno", # To be implemented, opencv etc
			"coffeeObservationUrl": coffeeObservationUrl,
			"newObservationFappened": newObservationFappened,
			"streaming": self.cameraStreamer.areWeCurrentlyStreaming(),
		}

	
	
	"""
	Checks if we should take a photo indeed
	
	@return (bool) 
	"""
	def shouldWeTakeAPhoto(self):
		howLongAgoLastShoot = self.cameraShooter.howManySecsAgoLastCapturingStarted()
		if howLongAgoLastShoot == 0 or howLongAgoLastShoot > 60:
			return True
		return False

	"""
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		return CameraShooter.shellApplicationRequirements + CameraStreamer.shellApplicationRequirements;

	"""
	Checks if we have coffe
	
	@param (dict) requestParams = None
	"""
	def checkForModeChangeRequests(self, requestParams = None):

		if requestParams is not None:
			if "message" in requestParams and "username" in requestParams:
				username = requestParams["username"]
				message = requestParams["message"]

				if username == "lsipii":
					if message.find("kahvibotti, laita streamaus päälle") > -1:
						if message.find("access code foxtrot tango whiskey") > -1:
							self.cameraStreamer.startStreaming()
					if message.find("kahvibotti, laita streamaus pois päältä") > -1:
						if message.find("access code whiskey tango foxtrot") > -1:
						

	
