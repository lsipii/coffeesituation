"""
@author lsipii
"""

"""App details container abstraction"""
class AppInfo:

	"""
	The base app name

	@var (string)
	"""
	baseAppName =  "TSH Coffee Situation"

	"""
	The base app version

	@var (string)
	"""
	baseAppVersion =  "v1.1"

	"""
	Gets the app version

	@return (string)
	"""
	def getAppVersion(self):
		return self.baseAppVersion

	"""
	Gets the full app name

	@return (string)
	"""
	def getFullAppName(self):
		return self.baseAppName + ": " + self.getAppIdent()

	"""
	Gets the app ident

	@return (string)
	"""
	def getAppIdent(self):
		return self.getAppName()+" "+self.getAppVersion()

	"""
	Gets the app name

	@return (string)
	"""
	def getAppName(self):
		raise Exception("The getAppName() name must be implemented")

	"""
	Gets the app mission statement

	@return (string)
	"""
	def getAppMissionStatement(self):
		raise Exception("The getAppMissionStatement() name must be implemented")

