#!/usr/bin/env python2
"""
@author lsipii
"""
from app.features.FacesBlurrer import FacesBlurrer

imageName = "abba.png"
imagePath = "app/data/testimages/"+imageName

facesBlurrer = FacesBlurrer()
facesBlurrer.blurFacesFromPicture(imagePath)
