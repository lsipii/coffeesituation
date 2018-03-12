#!/usr/bin/env python3
"""
@author lsipii
"""
import cv2
import numpy as np

from app.utils.images.filters.ImageBlurrer import ImageBlurrer

"""
Blurs an area

@see: https://stackoverflow.com/questions/15341538/numpy-opencv-2-how-do-i-crop-non-rectangular-region
@see: https://stackoverflow.com/questions/35783062/opencv-python-copy-polygon-from-one-image-to-another/35786923
"""
class AreaBlurrer(ImageBlurrer):

	"""
	Blurs the faces from image

	@param (string) imagePath
	"""
	def blurImage(self, imagePath):

		try:
			
			# Create opencv image
			cvImage = cv2.imread(imagePath)
		
			# check dimensions of the image
			height = np.size(cvImage, 0)
			width = np.size(cvImage, 1)

			# For now, use static points for blurring
			blurredAreaPoints = np.array([
				[(10,10), 
				(300,300), 
				(10,300)]
			], dtype=np.int32)

			# Create a black area mask the size of orig image
			srcMask = np.zeros(cvImage.shape, dtype = "uint8")

			# White polyfill the mask by blur points
			cv2.fillPoly(srcMask, [blurredAreaPoints], 255)

			# Create region of intrest, of the image, of the blur points
			roi = cvImage[np.min(blurredAreaPoints[:,1]):np.max(blurredAreaPoints[:,1]),np.min(blurredAreaPoints[:,0]):np.max(blurredAreaPoints[:,0])]
			mask = srcMask[np.min(blurredAreaPoints[:,1]):np.max(blurredAreaPoints[:,1]),np.min(blurredAreaPoints[:,0]):np.max(blurredAreaPoints[:,0])]
			"""
			# What is this
			invertedMask = cv2.bitwise_not(mask)
			background = cv2.bitwise_and(roi, roi, mask = invertedMask)
			sourceImageCuttedPart = cvImage[]
			src1_cut = src1[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]
			img2_fg = cv2.bitwise_and(src1_cut,src1_cut,mask = mask)
			"""

			
			# Write resulting image
			cv2.imwrite(imagePath, cvImage)

		except Exception as e:
			print(e)