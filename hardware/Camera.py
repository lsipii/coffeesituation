#!/usr/bin/env python3
"""
@author lsipii
"""
import sh
import base64 
import datetime

class Camera():

	"""
	Module initialization
	"""
	def __init__(self):
		self.photoShootTime = None

	"""
	Takes a photo
	
	@param (string) imagePath
	"""
	def takeAPhoto(self, imagePath):
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
		