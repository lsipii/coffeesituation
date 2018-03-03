#!/usr/bin/env python3
"""
@author lsipii
"""
class CoffeeQueryModeControl():

	"""
	Constructor

	@param (CoffeeChecker) checkerRef
	"""
	def __init__(self, checkerRef):
		self.coffeeChecker = checkerRef

		self.controlCommandLocale = None

		self.commandTranslations = {
			"stream": {
				"fi": {
					"command": ["streamaus ", "striimaus ", "stream "],
					"actions": {
						"ON": " päälle", 
						"OFF": [" pois", " veke"],
					}
				},
				"en": {
					"command": ["streaming ", " stream "],
					"actions": {
						"ON": [" on", "enable "], 
						"OFF": [" off", "disable "],
					}
				}
			}
		}

		self.accessTranslations = {
			"fi": {
				"accessCodePrefix": "turvasana"
			},
			"en": {
				"accessCodePrefix": "access code"
			}
		}
		
	"""
	Checks if we have coffe MODE change
	
	@param (dict) requestParams = None
	"""
	def checkForModeChangeRequests(self, requestParams = None):

		if requestParams is not None:
			if "message" in requestParams and "username" in requestParams:
				username = requestParams["username"]
				message = requestParams["message"]

				if self.checksIfAskingForAppControl(message):
					command = self.resolveAppControlCommand(message)
					if command is not None:
						if command == "stream":
							action = self.resolveAppControlCommandAction(command, message)
							if action is not None and self.canIHasAccessToAppModeCommand(username, message, command, action):
								if action == "ON": 
									self.coffeeChecker.cameraStreamer.startStreaming()
								elif action == "OFF":
									self.coffeeChecker.cameraStreamer.stopStreaming()
				self.controlCommandLocale = None
	
	"""
	Checks if we have coffe MODE change
	
	@param (string) message
	@retrun (bool)
	"""
	def checksIfAskingForAppControl(self, message):
		if message.find("kahvi") > -1:
			self.controlCommandLocale = "fi"
			return True
		elif message.find("coffee") > -1:
			self.controlCommandLocale = "en"
			return True
		return False

	"""
	Checks if we have coffe MODE change
	
	@param (string) message
	@retrun (string|None) resolvedCommandName
	"""
	def resolveAppControlCommand(self, message):
		resolvedCommandName = None
		if self.controlCommandLocale is not None:
			for commandName in self.commandTranslations:
				if self.controlCommandLocale in self.commandTranslations[commandName]:
					commandTranslation = self.commandTranslations[commandName][self.controlCommandLocale]["command"]
					if isinstance(commandTranslation, list):
						for translationPart in commandTranslation:
							if message.find(translationPart) > -1:
								resolvedCommandName = commandName
								break
						if resolvedCommandName is not None:
							break
					else:
						if message.find(commandTranslation) > -1:
							resolvedCommandName = commandName
							break
		return resolvedCommandName

	"""
	Checks if we have coffe MODE change
	
	@param (string) commandName
	@param (string) message
	@retrun (string|None) action
	"""
	def resolveAppControlCommandAction(self, commandName, message):

		action = None
		if self.controlCommandLocale in self.commandTranslations[commandName]:
			if "actions" in self.commandTranslations[commandName][self.controlCommandLocale]:
				for actionName in self.commandTranslations[commandName][self.controlCommandLocale]["actions"]:
					actionTranslation = self.commandTranslations[commandName][self.controlCommandLocale]["actions"][actionName]

					if isinstance(actionTranslation, list):
						for translationPart in actionTranslation:
							if message.find(translationPart) > -1:
								action = actionName
								break
						if action is not None:
							break
					else:
						if message.find(actionTranslation) > -1:
							action = actionName
							break
		return action

	"""
	Checks if user can access the given command
	
	@param (string) username
	@param (string) message
	@param (string) command
	@param (string) action = None
	@retrun (bool) accessGranted
	"""
	def canIHasAccessToAppModeCommand(self, username, message, command, action = None):

		accessGranted = False
		accessCodePrefix = self.accessTranslations[self.controlCommandLocale]["accessCodePrefix"]
		accssCodePrefixPos = message.find(accessCodePrefix)
		if accssCodePrefixPos > -1:
			if command == "stream" and action is not None:
				if action == "ON":
					if username == "lsipii":
						accessCodePos = message.find("foxtrot tango whiskey")
						accessGranted = accessCodePos > accssCodePrefixPos
				elif action == "OFF":
					if username == "lsipii":
						accessCodePos = message.find("whiskey tango foxtrot")
						accessGranted = accessCodePos > accssCodePrefixPos
		return accessGranted