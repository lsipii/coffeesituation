#!/usr/bin/env python3
"""
@author lsipii
"""
from hardware.CameraShots import CameraShots

class CoffeeChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.imageDirectory = "~/.zoinks/coffee"
		self.imageFilename = "cameraOutput.jpg"
		self.imagePath = self.imageDirectory+"/"+self.imageFilename
		self.camera = CameraShots(self.imageDirectory)

	"""
	Checks if we have coffe

	@return (bool) weHave
	"""
	def hasWeCoffee(self):

		if self.shouldWeTakeAPhoto(): 
			self.camera.takeAPhoto(self.imagePath)
		imageBinStr = self.camera.readImageAsB64String(self.imagePath)

		return {"message": "maybe?", "image": imageBinStr}

	
	
	"""
	Checks if we should take a photo indeed
	
	@return (bool) 
	"""
	def shouldWeTakeAPhoto(self):
		howLongAgoLastShoot = self.camera.howManySecsAgoLastCapturingStarted()
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
	
