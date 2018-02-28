#!/usr/bin/env python3
"""
@author lsipii
"""
from hardware.CameraShots import CameraShots
from hardware.MediaStorage import MediaStorage

class CoffeeChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.storage = MediaStorage({
			"driver": "local",
			"mediaDirectory": "/var/www/media/coffee",
			"mediaFilename": "zoinks.jpg",
			"mediaHost": "https://morphotic-cow-5470.dataplicity.io/images",
		})
		self.cameraShooter = CameraShots(self.storage)

	"""
	Checks if we have coffe

	@return (bool) weHave
	"""
	def hasWeCoffee(self):

		if self.shouldWeTakeAPhoto(): 
			self.cameraShooter.takeAPhoto()
		imageUrl = self.cameraShooter.getPhotoStorageUrl()

		return {"message": "maybe?", "image": imageUrl}

	
	
	"""
	Checks if we should take a photo indeed
	
	@return (bool) 
	"""
	def shouldWeTakeAPhoto(self):
		howLongAgoLastShoot = self.cameraShooter.howManySecsAgoLastCapturingStarted()
		if howLongAgoLastShoot == 0 or howLongAgoLastShoot > 30:
			return True
		return False

	"""
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		return CameraShots.shellApplicationRequirements;
	
