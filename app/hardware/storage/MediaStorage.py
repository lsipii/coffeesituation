#!/usr/bin/env python3
"""
@author lsipii
"""
import time

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

		self.driver = None
		self.configurations = {}
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

		if self.driver is None:
			raise Exception("Storage driver must be configured")

		self.setupDriverConfigurations(configs)

	"""
	Storage setup for local driver

	@param (dict) configs
	"""
	def setupDriverConfigurations(self, configs):
		raise Exception("Must be implemented")

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
		raise Exception("Must be implemented")
		
	"""
	Gets the media file path

	@return (string) mediaPath
	"""
	def getMediaFilePath(self):
		return self.configurations[self.driver]["mediaPath"]

	"""
	Gets the media file url

	@return (string) mediaUrl
	"""
	def getMediaFileUrl(self):
		return self.configurations[self.driver]["mediaUrl"]	

	"""
	Clears media folder from files
	"""
	def clearPreviousMediaFiles(self):
		raise Exception("Must be implemented")	

	"""
	Reads taken photo as base64 bin string
	
	@return (base64 string) image64
	"""
	def readImageAsB64String(self):
		
		import base64 
		imageRead = self.readImageAsBinary()
		image64 = base64.encodestring(imageRead)
		return image64

	"""
	Reads taken photo as base64 bin string
	
	@return (bin string) imageRead
	"""
	def readImageAsBinary(self):
		raise Exception("Must be implemented")