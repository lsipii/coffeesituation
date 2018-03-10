#!/usr/bin/env python3
"""
@author lsipii
"""
from app.hardware.Camera import Camera

import sh

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
		#sh.raspistill('-w', '640', '-h', '480', '-o', self.storage.getTemprorayMediaFilePath())
		sh.cp("/home/lsipii/Projects/tshzoink/app/data/testimages/5aa2867e.jpg", self.storage.getTemprorayMediaFilePath())
		super().captureStop()

	"""
	Returns the images url
	
	@return (string) imageUrl
	"""
	def getPhotoStorageUrl(self):
		return self.storage.getMediaFileUrl()
	
		