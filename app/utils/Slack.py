#!/usr/bin/env python3
"""
@author lsipii
"""
try:
	from urllib.parse import urljoin
	from urllib.parse import urlencode
	import urllib.request as urlrequest
except ImportError:
	from urlparse import urljoin
	from urllib import urlencode
	import urllib2 as urlrequest
import json

class Slack():

	"""
	Slack messanger

	@param (dict) config
	"""
	def __init__(self, config):
		self.config = config
		self.accessPoint = self.config["accessPoint"]
		self.defaultChannel = self.config["defaultChannel"]
		self.defaultUsername = self.config["defaultUsername"]
		self.defaultIcon = self.config["defaultIcon"]
		self.requestHandler = urlrequest.build_opener(urlrequest.HTTPHandler())


	"""
	Sends the gathered payload to slack

	@param (dict) payload, [message]
	"""
	def notify(self, payload):
		
		# Validate the payload
		if "message" not in payload:
			raise Exception("Slack.notify payload param must have a message")

		# Validate and set the channel
		channel = ("channel" in payload) and payload["channel"] or self.defaultChannel
		if not channel.startsWith("#"):
			channel = "#"+channel

		print(channel)
		
		self.sendSlackTextPayload({
			"message": payload["message"],
			"channel": channel,
			"username": ("username" in payload) and payload["username"] or self.defaultUsername,
			"icon": ("icon" in payload) and payload["icon"] or self.defaultIcon
		})


	"""
	Sends the text payload to slack

	@param (dict) payload, [message, channel, username, icon]
	@return (response)
	"""
	def sendSlackTextPayload(self, payload):

		payloadJson = json.dumps({
			"text": payload["message"],
			"channel": payload["channel"], 
			"username": payload["username"], 
			"icon_emoji": payload["icon"],
			"unfurl_media": False,
			"unfurl_links": False
		})
		
		data = urlencode({"payload": payloadJson})
		req = urlrequest.Request(self.accessPoint)
		response = self.requestHandler.open(req, data.encode('utf-8')).read()
		return response.decode('utf-8') 
