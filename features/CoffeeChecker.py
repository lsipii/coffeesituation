#!/usr/bin/env python3
"""
@author lsipii
"""
from hardware.CameraShots import CameraShots
from hardware.MediaStorage import MediaStorage
import random

class CoffeeChecker():

	"""
	Module initialization

	@param (dict) configs [storage]
	"""
	def __init__(self, configs):
		self.storage = MediaStorage(configs)
		self.cameraShooter = CameraShots(self.storage)
		self.coffeeMessages = [
			"I a badger. I know not many coffee things.",
			"For a cup of coffee there I would dans.",
			"If coffee is could I have as well?"
		]

	"""
	Checks if we have coffe

	@return (bool) weHave
	"""
	def hasWeCoffee(self):

		if self.shouldWeTakeAPhoto(): 
			self.cameraShooter.takeAPhoto() 
			imageUrl = self.cameraShooter.getPhotoStorageUrl()
			message = random.choice(self.coffeeMessages)
			slackNotice = message+" <"+imageUrl+"|Check the coffee situation here>"

			return {
				"message": message, 
				"image": imageUrl,
				"slackNotice": slackNotice
			}

		else:
			return {"message": "Situation has not changed"}

	
	
	"""
	Checks if we should take a photo indeed
	
	@return (bool) 
	"""
	def shouldWeTakeAPhoto(self):
		howLongAgoLastShoot = self.cameraShooter.howManySecsAgoLastCapturingStarted()
		if howLongAgoLastShoot == 0 or howLongAgoLastShoot > 60:
			return True
		return False

	"""
	Returns the list of required shell aps
	
	@return (array) 
	"""
	@staticmethod
	def getRequiredShellApps():
		return CameraShots.shellApplicationRequirements;
	
