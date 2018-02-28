#!/usr/bin/env python3
"""
@author lsipii
"""
from hardware.Camera import Camera

import sh
import base64 

class CameraShots(Camera):

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = ["raspistill"]

	"""
	Camera shots module initialization

	@param (string) storagePath
	"""
	def __init__(self, storagePath = None):
		super().__init__(storagePath)
		
	"""
	Takes a photo
	
	@param (string) imagePath
	"""
	def takeAPhoto(self, imagePath):
		super().captureStart()
		sh.raspistill('-o', imagePath)
		super().captureStop()

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
		