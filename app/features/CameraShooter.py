#!/usr/bin/env python3
"""
@author lsipii
"""
from app.hardware.Camera import Camera

import sh
import base64 

class CameraShooter(Camera):

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = ["raspistill"]

	"""
	Camera shots module initialization

	@param (MediaStorage) storage
	"""
	def __init__(self, storage):
		super().__init__()
		self.storage = storage
		
	"""
	Takes a photo
	"""
	def takeAPhoto(self):
		super().captureStart()
		self.storage.clearPreviousMediaFiles()
		self.storage.setupMediaFilename()
		sh.raspistill('-w', '640', '-h', '480', '-o', self.storage.getMediaFilePath())
		super().captureStop()

	"""
	Returns the images url
	
	@return (string) imageUrl
	"""
	def getPhotoStorageUrl(self):
		return self.storage.getMediaFileUrl()
	

	"""
	Reads taken photo as base64 bin string
	
	@return (base64 string) image64
	"""
	def readImageAsB64String(self):
		image = open(self.storage.getMediaFilePath(), 'rb') #open binary file in read mode
		imageRead = image.read()
		image64 = base64.encodestring(imageRead)
		return image64
		