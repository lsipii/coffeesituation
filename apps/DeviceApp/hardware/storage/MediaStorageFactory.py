#!/usr/bin/env python3
"""
@author lsipii
"""

class MediaStorageFactory():
	"""
	Creates a storage instance

	@param (dict) configs
	@param (string) wantsToHaveThisDriver = None
	@return (MediaStorage) storage
	"""
	@staticmethod
	def getInstance(configs, wantsToHaveThisDriver = None):
		if "storage_driver" in configs["app"]:

			if wantsToHaveThisDriver is None:
				storageDriver = configs["app"]["storage_driver"]
			else:
				storageDriver = wantsToHaveThisDriver

			if storageDriver == "local":
				from apps.DeviceApp.hardware.storage.LocalStorage import LocalStorage
				return LocalStorage(configs["storage"]["local"])
			elif storageDriver == "S3":
				from apps.DeviceApp.hardware.storage.S3Storage import S3Storage
				return S3Storage(configs["storage"]["S3"])
			else:
				raise Exception("Storage driver "+storageDriver+" not found")
		else:
			raise Exception("Storage driver must be configured")