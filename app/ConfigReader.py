#!/usr/bin/env python3
"""
@author lsipii
"""

import os
try:
    import json
except ImportError:
    import simplejson as json

"""Json configs reading helper"""
class ConfigReader:

	def __init__(self, secretsFileName = "settings", secretsFolder = "settings"):
		# From the app root, where the config files resides
		self.configurationFilesFolder = secretsFolder;
		# The config filename
		self.configurationFileName = secretsFileName
		# Read configs container
		self.config = None

	"""
	Generates app config dict

	@return (dict)
	"""
	def getConfig(self):
		if self.config is None:
			self.config = self.readConfigFile(self.configurationFileName, self.configurationFilesFolder)
		return self.config

	"""
	Read secrets from a settings/secretsFileName 
	"""
	def readConfigFile(self, secretsFileName, secretsFolder = None):

		if secretsFolder is None:
			secretsFolder = self.configurationFilesFolder

		try:
			# Ensure correct filename format
			if secretsFileName.find(secretsFolder+'/') == 0:
				secretsFileName = secretsFileName.replace(secretsFolder+'/', '')
			if secretsFileName.find('.json') == -1:
				secretsFileName = secretsFileName+".json"

			dir = os.path.dirname(__file__)
			secretsFilePath = os.path.join(dir, '..', secretsFolder, secretsFileName)

			with open(secretsFilePath) as dataFile:
				secrets = json.load(dataFile)

		except Exception as e:
			print("Reading settings file: "+secretsFileName+" failed...")
			print(e)
			exit(1)
		
		return secrets