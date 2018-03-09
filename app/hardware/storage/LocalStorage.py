#!/usr/bin/env python3
"""
@author lsipii
"""
import os
import sh
import glob
from app.hardware.storage.MediaStorage import MediaStorage

class LocalStorage(MediaStorage):

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = []

	"""
	Storage conf setups

	@param (dict) configs
	"""
	def setupDriverConfigurations(self, configs):

		self.configurations["local"] = {
			"mediaDirectory": None,
			"mediaFilename": None,
			"mediaPath": None,
			"mediaHost": None,	
			"mediaUrl": None,
		}

		if "mediaDirectory" in configs:
			self.configurations["local"]["mediaDirectory"] = configs["mediaDirectory"]
		if "mediaFilename" in configs:
			self.configurations["local"]["mediaFilename"] = configs["mediaFilename"]
		if "mediaHost" in configs:
			self.configurations["local"]["mediaHost"] = configs["mediaHost"]

		self.setupMediaFilename()

	
	"""
	Validates we'r good to go
	"""
	def validateStorageFunctionality(self):

		if self.configurations["local"]["mediaPath"] is None:
			raise Exception("Media path not initialized")
		if not os.access(self.configurations["local"]["mediaDirectory"], os.W_OK):
			raise Exception("No writing access to "+self.configurations["local"]["mediaDirectory"])

		# Ensure dir
		sh.mkdir("-p", self.configurations["local"]["mediaDirectory"])	
		
	"""
	Clears media folder from files
	"""
	def clearPreviousMediaFiles(self):
		files = glob.glob(self.configurations["local"]["mediaDirectory"]+"/*")
			for f in files:
				if os.path.isfile(f):
					os.unlink(f)	

	"""
	Reads taken photo as base64 bin string
	
	@return (bin string) imageRead
	"""
	def readImageAsBinary(self):
		image = open(self.getMediaFilePath(), 'rb') #open binary file in read mode
		imageRead = image.read()
		return imageRead