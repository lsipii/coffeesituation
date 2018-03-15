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

		self.driver = "S3"

		self.configurations[self.driver] = {
			"bucket": None,
			"mediaDirectory": "/coffee",
			"mediaFilename": None,
			"mediaPath": None,
			"mediaHost": None,	
			"mediaUrl": None,
		}

		if "AWS_S3_BUCKET" not in configs:
			raise Exception("Invalid S3 configurations")
		if "AWS_S3_ACCESS_KEY_ID" not in configs:
			raise Exception("Invalid S3 configurations")
		if "AWS_S3_SECRET_KEY" not in configs:
			raise Exception("Invalid S3 configurations")

		if "mediaDirectory" in configs:
			self.configurations[self.driver]["mediaDirectory"] = configs["mediaDirectory"]
		if "mediaHost" in configs:
			self.configurations[self.driver]["mediaHost"] = configs["mediaHost"]

		# Create an S3 client
		self.configurations[self.driver]["bucket"] = configs["AWS_S3_BUCKET"]	
		self.s3client = boto3.client('s3',
			aws_access_key_id=configs["AWS_S3_ACCESS_KEY_ID"],
			aws_secret_access_key=configs["AWS_S3_SECRET_KEY"],
		)
		
		# Setups the first pics name
		self.setupMediaFilename()

	
	"""
	Validates we'r good to go
	"""
	def validateStorageFunctionality(self):
		if self.configurations[self.driver]["bucket"] is None:
			raise Exception("S3 bucket not initialized")
		if self.configurations[self.driver]["mediaHost"] is None:
			raise Exception("S3 mediaHost not initialized")
		
	"""
	Clears media folder from files
	"""
	def clearPreviousMediaFiles(self):
		"""
		Disabled because GC happens with cron runs

		for bucketKeyObj in self.s3client.list_objects(Bucket=self.configurations[self.driver]["bucket"])['Contents']:
			if bucketKeyObj["Key"] != "404.jpg":
				self.s3client.delete_object(
					Bucket=self.configurations[self.driver]["bucket"],
					Key=bucketKeyObj["Key"]
				)
		"""
		return True

	"""
	Clears old media folder from files
	"""
	def clearTooOldMediaFiles(self):

		from datetime import datetime, timezone

		nowTime = datetime.now(timezone.utc)

		# How many seconds the pics are allowed to stand by
		picturesPersistanceInSeconds = 3600

		for bucketKeyObj in self.s3client.list_objects(Bucket=self.configurations[self.driver]["bucket"])['Contents']:
			if bucketKeyObj["Key"] != "404.jpg":
				dateTimeThen = bucketKeyObj["LastModified"]
				datediff = nowTime - dateTimeThen
				if datediff.total_seconds() > picturesPersistanceInSeconds:
					self.s3client.delete_object(
						Bucket=self.configurations[self.driver]["bucket"],
						Key=bucketKeyObj["Key"]
					)

	"""
	Saves the image file
	"""
	def saveImageFile(self):
		self.s3client.upload_fileobj(
			self.getImageFileObj(),
			self.configurations[self.driver]["bucket"],
			self.getMediaFilename(),
			ExtraArgs={
				"ContentType": "image/jpeg"
			}
		)