#!/usr/bin/env python3
"""
@author lsipii
"""
from app.hardware.Camera import Camera

import sh

class CameraStreamer(Camera):

	"""
	List of shell apps that we require

	@var (array) shellApplicationRequirements
	"""
	shellApplicationRequirements = ["motion"]

	"""
	Camera shots module initialization
	
	@param (dict) configs [app]
	"""
	def __init__(self, configs):
		super().__init__()
		self.streamingHost = configs["app"]["host"]
		self.weAreCurrentlyStreaming = False
		
	"""
	Starts the stream
	"""
	def startStreaming(self): 
		super().captureStart()
		self.weAreCurrentlyStreaming = True
		#sh.uv4l("-nopreview", "--auto-video_nr", "--driver", "raspicam", "--encoding", "mjpeg", "--width", "640", "--height", "480", "--framerate", "20", "--hflip=yes", "--vflip=yes", "--bitrate=2000000", "--server-option", "'--port=9090'", "--server-option", "'--max-queued-connections=30'", "--server-option", "'--max-streams=25'", "--server-option", "'--max-threads=29'")
		sh.sudo("service", "motion", "start")


	"""
	Stops the stream
	"""
	def stopStreaming(self):
		sh.sudo("service", "motion", "stop")
		super().captureStop()
		self.weAreCurrentlyStreaming = False

	"""
	Gets the streaming address

	@return (string) url
	"""
	def getStreamUrl(self):
		return self.streamingHost+"/stream"

	"""
	Checks if we're currently streaming

	@return (bool)
	"""
	def areWeCurrentlyStreaming(self):
		return self.weAreCurrentlyStreaming
		