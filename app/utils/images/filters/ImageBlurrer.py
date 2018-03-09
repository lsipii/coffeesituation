#!/usr/bin/env python3
"""
@author lsipii
"""

"""
Image blurring abstraction class
"""
class ImageBlurrer():

	"""
	@param (string) imagePath
	"""
	def blurImage(self, imagePath):
		raise NotImplementedError("ImageBlurrer class must have an blurImage(imagePath) method")
