#!/usr/bin/env python3
"""
@author lsipii
"""
import cv2
import numpy as np

from app.utils.Utils import getProjectRootPath
from app.utils.images.filters.ImageBlurrer import ImageBlurrer

"""
Blurs an area

@see: https://stackoverflow.com/questions/15341538/numpy-opencv-2-how-do-i-crop-non-rectangular-region
@see: https://stackoverflow.com/questions/35783062/opencv-python-copy-polygon-from-one-image-to-another/35786923
"""
class AreaBlurrer(ImageBlurrer):

	"""
	Initialization
	"""
	def __init__(self):
		super().__init__()
		self.spaceImagePath = getProjectRootPath()+"/app/data/images/space.jpg"

	"""
	Blurs the faces from image

	@param (string) imagePath
	"""
	def blurImage(self, imagePath):

		try:
			
			# Create opencv image
			spaceImage = cv2.imread(self.spaceImagePath)
			cvImage = cv2.imread(imagePath)

			# Dimensions
			height = np.size(cvImage, 0)
			width = np.size(cvImage, 1)

			# For now, use static points for blurring
			blurAreaPoints = [
				[0,0], 
				[0,284], 
				[67,217], 
				[100,144], 
				[178,128], 
				[250,133], 
				[331,124],
				[400,87],
				[480,110],
				[572,112],
				[width,163],
				[width,0],
			]
			blurredAreaPoints = np.array(blurAreaPoints, dtype=np.int32)

			#create a mask template
			srcMask = spaceImage.copy()
			srcMask = cv2.cvtColor(srcMask, cv2.COLOR_BGR2GRAY)
			srcMask.fill(0)

			# White polyfill the mask by blur points
			cv2.fillPoly(srcMask, [blurredAreaPoints], 255)

			# Create region of intrest, of the image, of the blur points
			roi = cvImage[np.min(blurredAreaPoints[:,1]):np.max(blurredAreaPoints[:,1]),np.min(blurredAreaPoints[:,0]):np.max(blurredAreaPoints[:,0])]
			mask = srcMask[np.min(blurredAreaPoints[:,1]):np.max(blurredAreaPoints[:,1]),np.min(blurredAreaPoints[:,0]):np.max(blurredAreaPoints[:,0])]

			# Cut and paste and combine
			invertedMask = cv2.bitwise_not(mask)
			spaceImageBackground = cv2.bitwise_and(roi, roi, mask = invertedMask)
			spaceImageCuttedPart = spaceImage[np.min(blurredAreaPoints[:,1]):np.max(blurredAreaPoints[:,1]),np.min(blurredAreaPoints[:,0]):np.max(blurredAreaPoints[:,0])]
			foregroundPart = cv2.bitwise_and(spaceImageCuttedPart, spaceImageCuttedPart, mask = mask)

			# Combine space triangle part and wanted coffee part, save as a final master piece
			destination = cv2.add(spaceImageBackground, foregroundPart)
			cvImageFinal = cvImage.copy()
			cvImageFinal[np.min(blurredAreaPoints[:,1]):np.max(blurredAreaPoints[:,1]),np.min(blurredAreaPoints[:,0]):np.max(blurredAreaPoints[:,0])] = destination

			# Write resulting images
			cv2.imwrite(imagePath, cvImageFinal)

		except Exception as e:
			print(e)