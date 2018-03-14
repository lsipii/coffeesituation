#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.coffee.CoffeeActionAccessChecker import CoffeeActionAccessChecker
from app.features.coffee.CoffeeSituationResolver import CoffeeSituationResolver
from app.features.CameraShooter import CameraShooter
from app.features.CameraStreamer import CameraStreamer
from app.hardware.storage.MediaStorageFactory import MediaStorageFactory

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs
	@param (bool) debugMode
	"""
	def __init__(self, configs, debugMode = False):
		self.storage = MediaStorageFactory.getInstance(configs)
		self.cameraShooter = CameraShooter(self.storage, debugMode)
		self.cameraStreamer = CameraStreamer(configs["app"])
		self.coffeeActionAccessChecker = CoffeeActionAccessChecker(configs["coffeeAccess"])
		self.coffeeSituationResolver = CoffeeSituationResolver(configs["app"]["settings"])
		self.initImageBlurrer(configs["app"]["settings"])


	"""
	Setups the image blurrer

	@param (dict) appSettings
	"""
	def initImageBlurrer(self, appSettings):
		
		self.imageBlurrer = None

		if "imageBlurrerFilter" in appSettings and appSettings['imageBlurrerFilter']:
			blurrerName = "app.utils.images.filters."+appSettings['imageBlurrerFilter']
			
			from app.utils.Utils import getModulePathInstance
			self.imageBlurrer = getModulePathInstance(blurrerName)
			

	"""
	Checks if we have coffe
	
	@param (dict) requestParams = None
	@return (dict) {
		(string) hasCoffee
		(string) coffeeObservationImageUrl
	}
	"""
	def hasWeCoffee(self, requestParams = None):

		# Check for mode change requests
		self.checkForModeChangeRequests(requestParams)

		# Get coffee data from selected service
		if self.cameraStreamer.areWeCurrentlyStreaming():
			coffeeObservationUrl = self.cameraStreamer.getStreamUrl()
		else:
			# Take the photo
			self.cameraShooter.takeAPhoto() 

			# Blur the photo, if the feat enabled
			if self.weHaveAnImageBlurrer(): 
				self.imageBlurrer.blurImage(self.storage.getTemprorayMediaFilePath())

			# Resolve the situation if resolving enabled
			if self.coffeeSituationResolver.isEnabled():
				self.coffeeSituationResolver.resolveCoffeeSituation(self.storage.getTemprorayMediaFilePath())
			
			# Store the photo
			self.storage.saveImageFile()

			# Grap the photo url
			coffeeObservationUrl = self.cameraShooter.getPhotoStorageUrl()

		# Coffee situation message

		return {
			"hasCoffeeMsg": self.coffeeSituationResolver.getCanWeHasCoffeeMsg(),
			"coffeeObservationUrl": coffeeObservationUrl,
			"streaming": self.cameraStreamer.areWeCurrentlyStreaming(),
		}

	"""
	Returns the list of required shell aps
	
	@return (array) {app}
	"""
	@staticmethod
	def getRequiredShellApps():
		return [CameraShooter, CameraStreamer]

	"""
	Checks if we have a coffee MODE change and executes it
	
	@param (dict) requestParams = None
	@return (dict) accessGrantedToCommandAction, {command, action}
	"""
	def checkForModeChangeRequests(self, requestParams = None):

		grantedAction = self.coffeeActionAccessChecker.getRequestedAndAllowedCommandAction(requestParams)
		if grantedAction["command"] is not None:
			if grantedAction["command"] == "stream":
				if grantedAction["action"] == "ON": 
					self.cameraStreamer.startStreaming()
				elif grantedAction["action"] == "OFF":
					self.cameraStreamer.stopStreaming()

	"""
	Checks if the image blurrer has been initialized

	@return bool
	"""
	def weHaveAnImageBlurrer(self):
		return self.imageBlurrer is not None

	"""
	Sets debug mode
	
	@param (bool) debugMode
	"""
	def setDebugMode(self, debugMode):
		self.debugMode = debugMode
		self.cameraShooter.setDebugMode(self.debugMode)
