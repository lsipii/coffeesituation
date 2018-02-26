#!/usr/bin/env python3
"""
@author lsipii
"""
import sh
import datetime

from hardware.Camera import Camera

class CoffeeChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.camera = Camera()
		self.imageDirectory = "~/.zoinks/coffee"
		self.imageFilename = "cameraOutput.jpg"
		self.imagePath = self.imageDirectory+"/"+self.imageFilename
		sh.mkdir("-p", self.imageDirectory)

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
		if self.camera.photoShootTime is None:
			return True

		howLongAgoLastShoot = datetime.now() - self.camera.photoShootTime
		if howLongAgoLastShoot.total_seconds() > 30:
			return True
			
		return False
