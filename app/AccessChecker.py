#!/usr/bin/env python3
"""
@author lsipii
"""
class AccessChecker():

	"""
	Module initialization
	"""
	def __init__(self):
		self.accessKey = "kyllig"

	"""
	Module initialization
	
	@param (string) accessKey
	@return (bool) accessGranted
	"""
	def ifAccessGranted(self, accessKey = None):
		if accessKey == self.accessKey:
			return True
		return False
		