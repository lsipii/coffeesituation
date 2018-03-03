#!/usr/bin/env python3
"""
@author lsipii
"""
class CoffeeActionAccessChecker():

	"""
	Constructor

	@param (dict) coffeeAccess
	"""
	def __init__(self, coffeeAccess):

		self.accessCodes = coffeeAccess

		self.controlCommandLocale = None
		self.controlLocales = ["fi", "en"]
		
		self.appModeAccessTranslations = {
			"fi": {
				"accessQueryKeywordPrefix": "kahvi",
				"accessCodePrefix": ["turvasana", "pääsyevättömyyskoodi", "tunnistautumiskoodi"]
			},
			"en": {
				"accessQueryKeywordPrefix": "coffee",
				"accessCodePrefix": "access code"
			}
		}

		self.commandTranslations = {
			"stream": {
				"fi": {
					"command": ["streamaus ", "striimaus ", "stream ", "striimi "],
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
	
	"""
	Checks if user can access the given command, action
	
	@param (string) username
	@param (string) message
	@param (string) command
	@param (string) action = None
	@retrun (bool) accessGranted
	"""
	def canIHasAccessToAppModeCommand(self, username, message, command, action = None):

		accessGranted = False
		if command in self.accessCodes:

			# Check that access code is tried
			accessCodePrefixTranslation = self.appModeAccessTranslations[self.controlCommandLocale]["accessCodePrefix"]
			accessCodePrefixTransData = self.getTranslationIndexData(accessCodePrefixTranslation, message)
			accessCodePrefixPos = accessCodePrefixTransData["index"]
			
			if accessCodePrefixPos > -1:
				
				commandAccessCodeData = self.accessCodes[command]
				if "actions" in commandAccessCodeData:
					if action is not None and action in commandAccessCodeData["actions"]:
						wantsAnAction = commandAccessCodeData["actions"][action]
						if username in wantsAnAction:
							accessCodePos = message.find(wantsAnAction[username])
							accessGranted = accessCodePos > accessCodePrefixPos
				
				# For commands that have no actions, also can override the actions access
				if not accessGranted and "access" in commandAccessCodeData:
					wantsAnAction = commandAccessCodeData["access"]
					if username in wantsAnAction:
						accessCodePos = message.find(wantsAnAction[username])
						accessGranted = accessCodePos > accessCodePrefixPos
		return accessGranted

	"""
	Checks and gets an coffee action if permitted
	
	@param (dict) requestParams = None
	@return (dict) accessGrantedToCommandAction, {command, action}
	"""
	def getRequestedAndAllowedCommandAction(self, requestParams = None):

		accessGrantedToCommandAction = {
			"command": None,
			"action": None,
		}

		if requestParams is not None:
			if "message" in requestParams and "username" in requestParams:
				username = requestParams["username"].lower()
				message = requestParams["message"].lower()

				if self.checksIfAskingForAppControl(message):
					command = self.resolveAppControlCommand(message)
					if command is not None:
						if command == "stream":
							action = self.resolveAppControlCommandAction(command, message)
							if action is not None and self.canIHasAccessToAppModeCommand(username, message, command, action):
								accessGrantedToCommandAction["command"] = command
								accessGrantedToCommandAction["action"] = action
				self.controlCommandLocale = None

		return accessGrantedToCommandAction
	
	"""
	Checks if we have a coffe MODE change, defines the query locale
	
	@param (string) message
	@retrun (bool)
	"""
	def checksIfAskingForAppControl(self, message):

		# Checks for control works that are prefixes to some other word, 
		# eg. for a keyword 'kahvi' we're at the point if input is 'kahvimörkö' or 'kahvia', but not when its only 'kahvi' 
		def controlCommandResolver(locale, message):
			controlTranslation = self.appModeAccessTranslations[locale]["accessQueryKeywordPrefix"]
			controlIndex = self.getTranslationIndexData(controlTranslation, message)
			if controlIndex["index"] > -1:
				if message[controlIndex["index"]+controlIndex["length"]:controlIndex["index"]+controlIndex["length"]+1].isalpha():
					self.controlCommandLocale = locale
					return True
			return False

		# Loop trough locales, break if a match
		for locale in self.controlLocales:
			if controlCommandResolver(locale, message):
				self.controlCommandLocale = locale
				return True
		return False

	"""
	Resolves the control command
	
	@param (string) message
	@retrun (string|None) resolvedCommandName
	"""
	def resolveAppControlCommand(self, message):
		resolvedCommandName = None
		if self.controlCommandLocale is not None:
			for commandName in self.commandTranslations:
				if self.controlCommandLocale in self.commandTranslations[commandName]:
					commandTranslation = self.commandTranslations[commandName][self.controlCommandLocale]["command"]
					commandIndex = self.getTranslationIndexData(commandTranslation, message)
					if commandIndex["index"] > -1:
						resolvedCommandName = commandName
						break
		return resolvedCommandName

	"""
	Resolves the control commands action
	
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
					actionIndex = self.getTranslationIndexData(actionTranslation, message)
					if actionIndex["index"] > -1:
						action = actionName
						break
		return action

	"""
	Gets the translations index and length if found from the message
	
	@param (string|array) translation
	@param (string) message
	@retrun (dict) {index, length}
	"""
	def getTranslationIndexData(self, translation, message):
		translationIndexData = {
			"index": -1,
			"length": 0,
		}
		if isinstance(translation, list):
			for translationPart in translation:
				partIndex = message.find(translationPart)
				if partIndex > -1:
					translationIndexData["index"] = partIndex
					translationIndexData["length"] = len(translationPart)
					break
		else:
			translationIndexData["index"] = message.find(translation)
			translationIndexData["length"] = len(translation)
		return translationIndexData
