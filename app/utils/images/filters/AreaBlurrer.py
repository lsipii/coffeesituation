#!/usr/bin/env python3
"""
@author lsipii
"""
import cv2
import numpy as np

from app.utils.images.filters.ImageBlurrer import ImageBlurrer

"""
Blurs an area
"""
class AreaBlurrer(ImageBlurrer):

	"""
	Blurs the faces from image

	@param (string) imagePath
	"""
	def blurImage(self, imagePath):

		# Create opencv image
		cvImage = cv2.imread(imagePath)
	
		# check dimensions of the image
		height = np.size(cvImage, 0)
		width = np.size(cvImage, 1)

		print(str(width) + " " + str(height))