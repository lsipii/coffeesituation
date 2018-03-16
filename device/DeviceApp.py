"""
@author lsipii
"""

from app.AppInfo import AppInfo
from app.ConfigReader import ConfigReader

"""App details container"""
class DeviceApp(AppInfo):

	"""
	App initialization
	"""
	def __init__(self):
		self.config = ConfigReader("settings").getConfig() 

	"""
	Gets the app name

	@return (string)
	"""
	def getAppName(self):
		return "Monitoring Device"

	"""
	Gets the app mission statement

	@return (string)
	"""
	def getAppMissionStatement(self):
		return "Monitor the secrets of the known universe"