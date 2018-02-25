#!/usr/bin/env python3
"""
@author lsipii
"""
import sh

class CoffeeChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.imageDirectory = "~/.zoinks/coffee"
		sh.mkdir("-p", self.imageDirectory)

	"""
	Checks if we have coffe

	@return (bool) weHave
	"""
	def hasWeCoffee(self):
		return {"message": "maybe?"}

	"""
	Takes a photo

	@return (string) imagePath
	"""
	def takeACoffeePhoto(self):
		imageDirectory
		imagePath=self.imageDirectory+"/cameraOutput.jpg"
		sh.raspistil('-o', imagePath)
		return imagePath