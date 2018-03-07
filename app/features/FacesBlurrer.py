#!/usr/bin/env python3
"""
@author lsipii
"""
import cv2

"""
Blurs faces

@see: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
"""
class FacesBlurrer():

	"""
	Constructor

	@param (dict) settings  = None
	"""
	def __init__(self, settings = None):
		self.faceCascade = cv2.CascadeClassifier('app/data/haarcascades/haarcascade_profileface.xml')
	
	"""
	Blurs the faces from image

	@param (string) imagePath
	"""
	def blurFacesFromPicture(self, imagePath):

		# Create opencv image, and a copy
		cvImage = cv2.imread(imagePath)
		resultingImage = cvImage.copy()

		# Detect faces
		cvImageGray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(cvImageGray, 1.3, 5)

		# Find out if there is faces, in the faces picture
		for (x,y,w,h) in faces:

			# Blur the face area
			facesArea = cvImage[y:y+h,x:x+w]
			facesArea = cv2.GaussianBlur(facesArea, (23, 23), 30)
			resultingImage[y:y+facesArea.shape[0], x:x+facesArea.shape[1]] = facesArea

		# Write resulting image
		cv2.imwrite(imagePath, resultingImage)