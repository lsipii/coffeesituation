#!/usr/bin/env python3
"""
@author lsipii
"""
from app.utils.images.filters.AreaBlurrer import AreaBlurrer

imageName = "mismoro.png"
imagePath = "app/data/testimages/"+imageName

areaBlurrer = AreaBlurrer()
areaBlurrer.blurImage(imagePath)
