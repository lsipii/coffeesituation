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
	Saves the image file
	"""
	def saveImageFile(self):
		raise Exception("Must be implemented")

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
	Gets the media file obj

	@return (FileObj) fileObj
	"""
	def getTemprorayMediaFileObj(self):
		return self.configurations[self.driver]["mediaPath"]

	"""
	Gets the media file url

	@return (string) mediaUrl
	"""
	def getMediaFileUrl(self):
		return self.configurations[self.driver]["mediaUrl"]	

	"""
	Gets the media filename

	@return (string) mediaUrl
	"""
	def getMediaFilename(self):
		return self.configurations[self.driver]["mediaFilename"]

	"""
	Temporary storage filepath

	@return (string) filepath
	"""
	def getTemprorayMediaFilePath(self):
		return self.getTemprorayMediaFolderPath()+"/"+self.getMediaFilename()
	
	"""
	Temporary storage path

	@return (string) dirpath
	"""
	def getTemprorayMediaFolderPath(self):
		return "/tmp"

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
		image = self.getImageFileObj()
		imageRead = image.read()
		return imageRead


	"""
	@return (fileObj)
	"""
	def getImageFileObj(self):
		return open(self.getTemprorayMediaFilePath(), 'rb') #open binary file in read mode