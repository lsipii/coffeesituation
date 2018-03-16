"""
@author lsipii
"""
from app.ConfigReader import ConfigReader
from app.AppInfo import AppInfo

"""App details container"""
class SlackBotApp(AppInfo):

	"""
	App initialization
	"""
	def __init__(self):
		self.config = ConfigReader("slackbot").getConfig() 

	"""
	Gets the app name

	@return (string)
	"""
	def getAppName(self):
		return "Coffee Related Communication And Relations Facilitator"

	"""
	Gets the app mission statement

	@return (string)
	"""
	def getAppMissionStatement(self):
		return "Facilitate communication between species and put an end to hostilities"