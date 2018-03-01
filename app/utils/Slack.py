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

	@param (dict) configs
	"""
	def __init__(self, configs):
		self.config = configs
		self.requestHandler = urlrequest.build_opener(urlrequest.HTTPHandler())


	"""
	Sends the gathered payload to slack

	@param (dict) payload, [message, channel, network]
	@return (response)
	"""
	def notify(self, payload):
		
		# Validate the payload
		if "message" not in payload:
			raise Exception("Slack.notify payload param must have a message")
		if "network" not in payload:
			raise Exception("Slack.notify payload param must have a network to select from configs")

		# Validate and set the channel
		channel = ("channel" in payload) and payload["channel"] or self.configs[payload["network"]]["defaultChannel"]
		if not channel.startswith("#"):
			channel = "#"+channel

		return self.sendSlackTextPayload({
			"message": payload["message"],
			"channel": channel,
			"username": ("username" in payload) and payload["username"] or self.configs[payload["network"]]["defaultUsername"],
			"icon": ("icon" in payload) and payload["icon"] or self.configs[payload["network"]]["defaultIcon"],
			"accessPoint": self.configs[payload["network"]]["accessPoint"]
		})


	"""
	Sends the text payload to slack

	@param (dict) payload, [message, channel, username, icon, accessPoint]
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
		req = urlrequest.Request(payload["accessPoint"])
		response = self.requestHandler.open(req, data.encode('utf-8')).read()
		return response.decode('utf-8') 
