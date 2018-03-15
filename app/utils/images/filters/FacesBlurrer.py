#!/usr/bin/env python3
"""
@author lsipii
"""
import cv2
from app.utils.images.filters.ImageBlurrer import ImageBlurrer

"""
Blurs faces

@see: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
"""
class FacesBlurrer(ImageBlurrer):

	"""
	Constructor

	@param (dict) settings  = None
	"""
	def __init__(self, settings = None):
		self.faceCascade = cv2.CascadeClassifier(getProjectRootPath()+'/app/data/haarcascades/haarcascade_frontalface_default.xml')
	
	"""
	Blurs the faces from image

	@param (string) imagePath
	"""
	def blurImage(self, imagePath):

		try:
		
			# Read and transform imagePath file to an opencv image matrix
			cvImage = cv2.imread(imagePath)
		
			# Detect faces
			cvImageGray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
			faces = self.faceCascade.detectMultiScale(cvImageGray, 
				scaleFactor=1.1, 
				minNeighbors=5,
				minSize=(30, 30),
				flags = cv2.CASCADE_SCALE_IMAGE
			)

			# Find out if there is faces, in the faces picture
			if len(faces) > 0:

				# Blur faces
				for (x,y,w,h) in faces:
					
					# Blur the face area
					facesArea = cvImage[y:y+h,x:x+w]
					facesArea = cv2.GaussianBlur(facesArea, (23, 23), 30)
					cvImage[y:y+facesArea.shape[0], x:x+facesArea.shape[1]] = facesArea

				# Write resulting image
				cv2.imwrite(imagePath, cvImage)
				
		except Exception as e:
			print(e)