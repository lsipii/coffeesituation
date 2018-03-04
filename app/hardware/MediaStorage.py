#!/usr/bin/env python3
"""
@author lsipii
"""
import os
import sh
import time
import glob

class MediaStorage():

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = []

	"""
	Storage constructor

	@param (dict) configs
	"""
	def __init__(self, configs = None):

		self.driver = "local"

		self.configurations = {
			"local": {
				"mediaDirectory": None,
				"mediaFilename": None,
				"mediaPath": None,
				"mediaHost": None,	
				"mediaUrl": None,
			}
		}
		
		self.imageExtension = "jpg"

		if configs is not None:
			self.setupStorage(configs)

	"""
	Storage setup

	@param (dict) configs
	"""
	def setupStorage(self, configs):
		if "driver" in configs:
			self.driver = configs["driver"]

		if self.driver == "local":
			self.setupLocalDriverConfigurations(configs)

	"""
	Storage setup for local driver

	@param (dict) configs
	"""
	def setupLocalDriverConfigurations(self, configs):
		if "mediaDirectory" in configs:
			self.configurations["local"]["mediaDirectory"] = configs["mediaDirectory"]
		if "mediaFilename" in configs:
			self.configurations["local"]["mediaFilename"] = configs["mediaFilename"]
		if "mediaHost" in configs:
			self.configurations["local"]["mediaHost"] = configs["mediaHost"]

		self.setupMediaFilename()

	"""
	Setups media filename
	"""
	def setupMediaFilename(self):

		stampBase64 = "{0:x}".format(int(time.time()))
		self.configurations[self.driver]["mediaFilename"] = stampBase64+"."+self.imageExtension

		if self.configurations[self.driver]["mediaDirectory"] is not None:
			self.configurations[self.driver]["mediaPath"] = self.configurations[self.driver]["mediaDirectory"]+"/"+self.configurations[self.driver]["mediaFilename"]
		if self.configurations[self.driver]["mediaHost"] is not None:
			self.configurations[self.driver]["mediaUrl"] = self.configurations[self.driver]["mediaHost"]+"/"+self.configurations[self.driver]["mediaFilename"]

	"""
	Validates we'r good to go
	"""
	def validateStorageFunctionality(self):

		if self.driver == "local":
			if self.configurations["local"]["mediaPath"] is None:
				raise Exception("Media path not initialized")
			if not os.access(self.configurations["local"]["mediaDirectory"], os.W_OK):
				raise Exception("No writing access to "+self.configurations["local"]["mediaDirectory"])

			# Ensure dir
			sh.mkdir("-p", self.configurations["local"]["mediaDirectory"])
		else:
			raise Exception("Storage driver "+self.driver+" not supported")	
		
	"""
	Gets the media file path

	@return (string) mediaPath
	"""
	def getMediaFilePath(self):
		if self.driver == "local":
			return self.configurations["local"]["mediaPath"]
		else:
			raise Exception("Storage driver "+self.driver+" not supported")	

	"""
	Gets the media file url

	@return (string) mediaUrl
	"""
	def getMediaFileUrl(self):
		if self.driver == "local":
			return self.configurations["local"]["mediaUrl"]
		else:
			raise Exception("Storage driver "+self.driver+" not supported")	

	"""
	Clears media folder from files
	"""
	def clearPreviousMediaFiles(self):
		if self.driver == "local":
			files = glob.glob(self.configurations["local"]["mediaDirectory"]+"/*")
			for f in files:
				if os.path.isfile(f):
					os.unlink(f)
		else:
			raise Exception("Storage driver "+self.driver+" not supported")	

	"""
	Reads taken photo as base64 bin string
	
	@return (base64 string) image64
	"""
	def readImageAsB64String(self):
		
		import base64 

		if self.driver == "local":
			imageRead = self.readImageAsBinary()
			image64 = base64.encodestring(imageRead)
			return image64
		else:
			raise Exception("Storage driver "+self.driver+" not supported")

	"""
	Reads taken photo as base64 bin string
	
	@return (bin string) imageRead
	"""
	def readImageAsBinary(self):
		
		if self.driver == "local":
			image = open(self.getMediaFilePath(), 'rb') #open binary file in read mode
			imageRead = image.read()
			return imageRead
		else:
			raise Exception("Storage driver "+self.driver+" not supported")