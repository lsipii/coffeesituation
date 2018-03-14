#!/usr/bin/env python3
"""
@author lsipii
"""
from app.hardware.RaspiCamera import RaspiCamera


class CameraShooter(RaspiCamera):

	"""
	Camera shots module initialization

	@param (MediaStorage) storage
	@param (bool) debugMode
	"""
	def __init__(self, storage, debugMode = False):
		super().__init__(debugMode)
		self.storage = storage
		
	"""
	Takes a photo
	"""
	def takeAPhoto(self, mediaPath = None):
		super().captureStart()
		self.storage.clearPreviousMediaFiles()
		self.storage.setupMediaFilename()
		super().takeAPhoto(self.storage.getTemprorayMediaFilePath())
		super().captureStop()

	"""
	Returns the images url
	
	@return (string) imageUrl
	"""
	def getPhotoStorageUrl(self):
		return self.storage.getMediaFileUrl()
	
		