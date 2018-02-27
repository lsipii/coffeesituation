#!/usr/bin/env python3
"""
@author lsipii
"""

"""
Validate shell apps

@throws (Exception)
@param (list|string) requiredApps
"""
def validateAppRequirements(requiredApps):

	from shutil import which

	if isinstance(requiredApps, str):
		requiredApps = [requiredApps]

	for appName in requiredApps:
		appPath=which(appName)
		if appPath is None:
			raise Exception("You must have command line app \'"+appName+"\' installed!")
