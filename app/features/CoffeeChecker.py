#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.CameraShooter import CameraShooter
from app.hardware.MediaStorage import MediaStorage

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs [storage]
	"""
	def __init__(self, configs):
		self.storage = MediaStorage(configs)
		self.cameraShooter = CameraShooter(self.storage)
		self.previousChannel = None

	"""
	Checks if we have coffe
	
	@param (dict) requestParams, [channel]
	@return (dict) {
		(string) hasCoffee
		(string) coffeeObservationImageUrl
		(bool) newObservationFappened
	}
	"""
	def hasWeCoffee(self, requestParams):

		newObservationFappened = False
		if self.shouldWeTakeAPhoto(): 
			self.cameraShooter.takeAPhoto() 
			newObservationFappened = True
		elif self.observedFromDifferenctChannel(requestParams):
			newObservationFappened = True
			
		coffeeObservationImageUrl = self.cameraShooter.getPhotoStorageUrl()
		
		# Mark the channel for the next query
		if newObservationFappened and "channel" in requestParams:
			self.previousChannel = requestParams["channel"]

		return {
			"hasCoffee": "dunno",
			"coffeeObservationImageUrl": coffeeObservationImageUrl,
			"newObservationFappened": newObservationFappened
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
	Checks if the previous check was not from the currently requested channel
	
	@param (dict) requestParams, [channel]
	@return (bool) 
	"""
	def shouldWeTakeAPhoto(self, requestParams):
		if "channel" in requestParams and requestParams["channel"] is not self.previousChannel:
			return True
		return False

	"""
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		return CameraShooter.shellApplicationRequirements;
	
