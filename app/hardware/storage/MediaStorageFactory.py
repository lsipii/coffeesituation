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
		if "driver" in configs:
			if configs["driver"] == "local":
				from app.hardware.storage.LocalStorage import LocalStorage
				return LocalStorage(configs)
			elif configs["driver"] == "s3":
				from app.hardware.storage.S3Storage import S3Storage
				return S3Storage(configs)
			else:
				raise Exception("Storage driver "+configs["driver"]+" not found")
		else:
			raise Exception("Storage driver must be configured")