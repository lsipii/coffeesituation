#!/usr/bin/env python3
"""
@author lsipii
"""

import sh

from device.hardware.Camera import Camera

class RaspiCamera(Camera):

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = ["raspistill"]

	"""
	Takes a photo

	@param (string) savePath
	"""
	def takeAPhoto(self, savePath):
		if self.shellApplicationRequirementsMet:
			if self.debugMode:
				print("Taking a real photo")
			sh.raspistill('-w', '640', '-h', '480', '-o', savePath)
		elif self.debugMode:
			print("Taking a fake photo")
			self.takeADebugPhoto(savePath)