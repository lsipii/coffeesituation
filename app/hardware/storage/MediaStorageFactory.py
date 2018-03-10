#!/usr/bin/env python3
"""
@author lsipii
"""

class MediaStorageFactory():
	"""
	Creates a storage instance

	@param (dict) configs
	@return (MediaStorage) storage
	"""
	@staticmethod
	def getInstance(configs):
		if "storage_driver" in configs["app"]:
			if configs["app"]["storage_driver"] == "local":
				from app.hardware.storage.LocalStorage import LocalStorage
				return LocalStorage(configs["storage"]["local"])
			elif configs["app"]["storage_driver"] == "S3":
				from app.hardware.storage.S3Storage import S3Storage
				return S3Storage(configs["storage"]["S3"])
			else:
				raise Exception("Storage driver "+configs["app"]["storage_driver"]+" not found")
		else:
			raise Exception("Storage driver must be configured")