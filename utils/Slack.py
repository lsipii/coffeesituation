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
		self.accessPoint = configs["accessPoint"]
		self.channel = configs["channel"]
		self.username = configs["username"]
		self.icon = configs["icon"]
		self.requestHandler = urlrequest.build_opener(urlrequest.HTTPHandler())

	"""
	Sends message to slack
	
	@param (string) message
	"""
	def send(self, message):

		payload_json = json.dumps({
			"text": message,
			"channel": self.channel, 
			"username": self.username, 
			"icon_emoji": self.icon
		})
		
		data = urlencode({"payload": payload_json})
		req = urlrequest.Request(self.accessPoint)
		response = self.requestHandler.open(req, data.encode('utf-8')).read()
		return response.decode('utf-8')