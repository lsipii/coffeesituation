#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.CameraShooter import CameraShooter
from app.hardware.MediaStorage import MediaStorage
import random

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs [storage]
	"""
	def __init__(self, configs):
		self.storage = MediaStorage(configs)
		self.cameraShooter = CameraShooter(self.storage)

	"""
	Checks if we have coffe

	@return (dict) {
		(string) hasCoffee
		(string) coffeeObservationImageUrl
		(bool) newObservationFappened
	}
	"""
	def hasWeCoffee(self):

		newObservationFappened = False
		if self.shouldWeTakeAPhoto(): 
			self.cameraShooter.takeAPhoto() 
			newObservationFappened = True
			
		coffeeObservationImageUrl = self.cameraShooter.getPhotoStorageUrl()
			
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
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		return CameraShooter.shellApplicationRequirements;
	
