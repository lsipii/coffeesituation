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


"""
Imports the modulePath module, creates and returns an instance

@param (string) modulePath
@param (list) *args
@return (module) 
"""
def getModulePathInstance(modulePath, *args):
	import importlib
	className = modulePath.split('.')[-1]
	executorModule = importlib.import_module(modulePath)
	executorClass = getattr(executorModule, className)
	return executorClass(*args)