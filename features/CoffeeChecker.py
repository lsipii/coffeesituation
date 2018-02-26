#!/usr/bin/env python3
"""
@author lsipii
"""
import sh
import base64 
import datetime

class CoffeeChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.photoShootTime = None
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
			self.takeACoffeePhoto(self.imagePath)
		imageBinStr = self.readImageAsB64String(self.imagePath)

		return {"message": "maybe?", "image": imageBinStr}

	
	
	"""
	Checks if we should take a photo indeed
	
	@return (bool) 
	"""
	def shouldWeTakeAPhoto(self, imagePath):
		if self.photoShootTime is None
			return True

		howLongAgoLastShoot = datetime.now() - self.photoShootTime
		if howLongAgoLastShoot.total_seconds() > 30:
			return True
			
		return False
		

	"""
	Takes a photo
	
	@param (string) imagePath
	"""
	def takeACoffeePhoto(self, imagePath):
		self.photoShootTime = datetime.now()
		sh.raspistil('-o', imagePath)

	"""
	Reads taken photo as base64 bin string
	
	@param (string) imagePath
	@return (base64 string) image64
	"""
	def readImageAsB64String(self, imagePath):
		image = open(imagePath, 'rb') #open binary file in read mode
		imageRead = image.read()
		image64 = base64.encodestring(imageRead)
		return image64