#!/usr/bin/env python3
"""
@author lsipii
"""
from datetime import datetime
import sh

class Camera():

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = []

	"""
	Flags that app requirements are met

	@var (bool) shellApplicationRequirementsMet
	"""
	shellApplicationRequirementsMet = True

	"""
	Camera module initialization

	"""
	def __init__(self, debugMode = False):

		# Debug mode setting
		self.debugMode = debugMode

		# Times, good times
		self.times = {
			"captureStartTime": None, # timedate
			"captureStopTime": None, # timedate
			"captureTotalTime": None, # timedelta
			"captureTimesResetTime": None, # timedate
		}

	"""
	Takes a photo

	@param (string) savePath
	"""
	def takeAPhoto(self, savePath):
		raise Exception("Camera.takeAPhoto(savePath): Must be implemented")

	"""
	Fakes a photoshoot

	@param (string) savePath
	"""
	def takeADebugPhoto(self, savePath):
		sh.cp("./app/data/testimages/5aa2867e.jpg", savePath)

	"""
	Start shooting
	"""
	def captureStart(self):
		self.times["captureStartTime"] = datetime.now()
		self.times["captureTimesResetTime"] = self.times["captureStartTime"] # Note that python datetime getters are immutable, this is a copy

	
	"""
	Stop shooting
	"""
	def captureStop(self):

		# Lil validation
		if self.hasNotCapturedAtAll():
			raise Exception('Camera.cameraStop must be called after cameraStart!')

		self.times["captureStopTime"] = datetime.now()
		self.times["captureTotalTime"] = self.times["captureStopTime"] - self.times["captureStartTime"]


	"""
	Reset, restart shooting
	"""
	def captureRestart(self):
		self.times["captureStopTime"] = None
		self.times["captureTotalTime"] = None
		self.captureStart()

	"""
	Checks if there has been any camera usage on runtime

	@return (bool) 
	"""
	def hasNotCapturedAtAll(self):
		return self.howManySecsAgoLastCapturingStarted() == 0

	"""
	Checks how long time ago was the last frames capturing started

	@return (int) 
	"""
	def howManySecsAgoLastCapturingStarted(self):
		return self.howManySecsAgoWasLastCameraSomething("captureStartTime")

	"""
	Checks how long time ago was the something something something

	@return (int) 
	"""
	def howManySecsAgoWasLastCameraSomething(self, timeObjName):

		timeObj = self.getTimeObj(timeObjName)
		if timeObj is None:
			return 0

		difference = datetime.now() - timeObj #  Note: returns timedelta obj
		return difference.total_seconds()

	"""
	Get shooting time obj by name

	@param (string) timeObjName
	@return (datetime|timedelta)
	"""
	def getTimeObj(self, timeObjName):
		# Lil validation
		if timeObjName not in self.times:
			raise Exception("No timeObjName "+timeObjName+" defined in Camera.times dict")
		return self.times[timeObjName]

	"""
	Sets debug mode
	
	@param (bool) debugMode
	"""
	def setDebugMode(self, debugMode):
		self.debugMode = debugMode
	

