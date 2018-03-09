#!/usr/bin/env python3
"""
@author lsipii
"""
import boto3
from app.hardware.storage.MediaStorage import MediaStorage

class S3Storage(MediaStorage):

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

		# Create an S3 client
		self.s3client = boto3.client('s3')

		self.configurations["S3"] = {
			"bucket": None,
			"mediaDirectory": "/",
			"mediaFilename": None,
			"mediaPath": None,
			"mediaHost": None,	
			"mediaUrl": None,
		}

		if "bucket" in configs:
			self.configurations["S3"]["bucket"] = configs["bucket"]
		if "mediaDirectory" in configs:
			self.configurations["S3"]["mediaDirectory"] = configs["mediaDirectory"]
		if "mediaHost" in configs:
			self.configurations["S3"]["mediaHost"] = configs["mediaHost"]

		self.setupMediaFilename()

	
	"""
	Validates we'r good to go
	"""
	def validateStorageFunctionality(self):
		if self.configurations["S3"]["bucket"] is None:
			raise Exception("S3 bucket not initialized")
		if self.configurations["S3"]["mediaHost"] is None:
			raise Exception("S3 mediaHost not initialized")
		
	"""
	Clears media folder from files
	"""
	def clearPreviousMediaFiles(self):
		files = glob.glob(self.configurations["S3"]["mediaDirectory"]+"/*")
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