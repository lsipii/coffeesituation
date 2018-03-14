#!/usr/bin/env python3
"""
@author lsipii
"""

import sh

from app.hardware.Camera import Camera

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
			sh.raspistill('-w', '640', '-h', '480', '-o', savePath)
		elif self.debugMode:
			self.takeADebugPhoto(savePath)