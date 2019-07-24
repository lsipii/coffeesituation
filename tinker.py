#!/usr/bin/env python3
"""
@author lsipii
"""
from apps.utils.images.filters.AreaBlurrer import AreaBlurrer

imageName = "mismoro.png"
imagePath = "device/data/testimages/"+imageName

areaBlurrer = AreaBlurrer()
areaBlurrer.blurImage(imagePath)
