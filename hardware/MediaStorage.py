#!/usr/bin/env python3
"""
@author lsipii
"""
import os
import sh

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

		if self.configurations["local"]["mediaDirectory"] is not None and self.configurations["local"]["mediaFilename"] is not None:
			self.configurations["local"]["mediaPath"] = self.configurations["local"]["mediaDirectory"]+"/"+self.configurations["local"]["mediaFilename"]
		if self.configurations["local"]["mediaHost"] is not None and self.configurations["local"]["mediaFilename"] is not None:
			self.configurations["local"]["mediaUrl"] = self.configurations["local"]["mediaHost"]+"/"+self.configurations["local"]["mediaFilename"]

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

	"""
	Gets the media file url

	@return (string) mediaUrl
	"""
	def getMediaFileUrl(self):
		if self.driver == "local":
			return self.configurations["local"]["mediaUrl"]
		return None
