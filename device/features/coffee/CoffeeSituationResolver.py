#!/usr/bin/env python3
"""
@author lsipii
"""
import cv2
import numpy as np

"""
Checks if there is coffee using Haar classification

@see: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
@see: https://github.com/jordanott/Coffee-Robot
"""
class CoffeeSituationResolver():

	"""
	Constructor

	@param (dict) settings, {CoffeeSituationResolverEnabled}
	"""
	def __init__(self, settings):
		self.imagePath = None
		self.coffeeSituationResolverEnabled = settings["CoffeeSituationResolverEnabled"]
		self.coffeeAwarenessMsg = "no data"

		self.coffeePotCascade = None
		self.liquidAreaCascade = None
		
		if self.coffeeSituationResolverEnabled:
			self.coffeePotCascade = cv2.CascadeClassifier('app/data/haarcascades/coffeePots.xml')
			self.liquidAreaCascade = cv2.CascadeClassifier('app/data/haarcascades/liquids.xml')

	"""
	Checks if the feat is enabled

	@return (bool)
	"""
	def isEnabled(self):
		return self.coffeeSituationResolverEnabled

	"""
	Reads the image data for some indicators that we should have coffee, maybe?

	@return (string) coffeeAwarenessMsg = not recognized
	"""
	def getCanWeHasCoffeeMsg(self):
		return self.coffeeAwarenessMsg

	"""
	Resolves the coffee situation message

	@param (string) imagePath
	"""
	def resolveCoffeeSituation(self, imagePath):
		
		# Default situation
		self.coffeeAwarenessMsg = "Not recognized"
		
		# Read and transform imagePath file to an opencv image matrix
		cvImage = cv2.imread(imagePath)
		cvImageGray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)

		# Detect coffee pots
		coffeePots = self.coffeePotCascade.detectMultiScale(cvImageGray, 1.3, 5)

		# Find out if there is coffee, in the coffee pots
		for (x,y,w,h) in coffeePots:

			# Coffeepot area
			coffeePotAreaImageGray = cvImageGray[y:y+h,x:x+w]

			# Find the liquid areas
			potsLiquidAreas = self.liquidAreaCascade.detectMultiScale(coffeePotAreaImageGray, 1.3, 5)
			
			# Calc blackness of the liquids
			rgbMean = 0
			for (lx,ly,lw,lh) in potsLiquidAreas:
				liquidColours = cvImage[ly:ly+lh, lx:lx+lw]
				means = cv2.mean(liquidColours)
				rgbMean += means[0] + means[1] + means[2]

			# If dark enough, we should have coffee
			if rgbMean > 0 and rgbMean < 100:
				self.coffeeAwarenessMsg = "We might have coffee"

		return self.coffeeAwarenessMsg