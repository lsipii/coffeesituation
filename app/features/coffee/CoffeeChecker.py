#!/usr/bin/env python3
"""
@author lsipii
"""
from app.features.coffee.CoffeeActionAccessChecker import CoffeeActionAccessChecker
from app.features.coffee.CoffeeSituationResolver import CoffeeSituationResolver
from app.features.CameraShooter import CameraShooter
from app.features.CameraStreamer import CameraStreamer
from app.features.FacesBlurrer import FacesBlurrer
from app.hardware.MediaStorage import MediaStorage

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs [storage]
	"""
	def __init__(self, configs):
		self.storage = MediaStorage(configs["storage"])
		self.cameraShooter = CameraShooter(self.storage)
		self.cameraStreamer = CameraStreamer(configs["app"])
		self.coffeeActionAccessChecker = CoffeeActionAccessChecker(configs["coffeeAccess"])
		self.coffeeSituationResolver = CoffeeSituationResolver(configs["app"]["settings"])
		self.facesBlurrer = FacesBlurrer()

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
			if self.coffeeSituationResolver.isEnabled():
				self.coffeeSituationResolver.setImageData()
		else:
			self.cameraShooter.takeAPhoto()  
			self.facesBlurrer.blurFacesFromPicture(self.storage.getMediaFilePath())
			coffeeObservationUrl = self.cameraShooter.getPhotoStorageUrl()
			if self.coffeeSituationResolver.isEnabled():
				self.coffeeSituationResolver.setImageData(self.storage.readImageAsBinary())
		
		# Coffee situation message
		hasCoffeeMsg = self.coffeeSituationResolver.getCanWeHasCoffeeMsg()

		return {
			"hasCoffeeMsg": hasCoffeeMsg,
			"coffeeObservationUrl": coffeeObservationUrl,
			"streaming": self.cameraStreamer.areWeCurrentlyStreaming(),
		}

	"""
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		apps = CameraShooter.shellApplicationRequirements + CameraStreamer.shellApplicationRequirements
		return apps

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