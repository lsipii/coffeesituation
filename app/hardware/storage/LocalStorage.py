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

		self.driver = "local"
		
		self.configurations[self.driver] = {
			"mediaDirectory": None,
			"mediaFilename": None,
			"mediaPath": None,
			"mediaHost": None,	
			"mediaUrl": None,
		}

		if "mediaDirectory" in configs:
			self.configurations[self.driver]["mediaDirectory"] = configs["mediaDirectory"]
		if "mediaFilename" in configs:
			self.configurations[self.driver]["mediaFilename"] = configs["mediaFilename"]
		if "mediaHost" in configs:
			self.configurations[self.driver]["mediaHost"] = configs["mediaHost"]

		self.setupMediaFilename()

	
	"""
	Validates we'r good to go
	"""
	def validateStorageFunctionality(self):

		if self.configurations[self.driver]["mediaPath"] is None:
			raise Exception("Media path not initialized")
		if not os.access(self.configurations[self.driver]["mediaDirectory"], os.W_OK):
			raise Exception("No writing access to "+self.configurations[self.driver]["mediaDirectory"])

		# Ensure dir
		sh.mkdir("-p", self.configurations[self.driver]["mediaDirectory"])	
		
	
	"""
	Saves the image file
	"""
	def saveImageFile(self):
		sh.mv(self.getTemprorayMediaFilePath(), self.getMediaFilePath())

	"""
	Clears media folder from files
	"""
	def clearPreviousMediaFiles(self):
		files = glob.glob(self.configurations[self.driver]["mediaDirectory"]+"/*")
		for f in files:
			if os.path.isfile(f):
				os.unlink(f)
