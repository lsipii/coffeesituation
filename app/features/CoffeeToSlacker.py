#!/usr/bin/env python3
"""
@author lsipii
"""
import random
from app.utils.Slack import Slack

class CoffeeToSlacker(Slack):

	"""
	Slack messanger, coffee overrides

	@param (dict) config
	"""
	def __init__(self, config):
		super().__init__(config)

		# Define coffee messages
		self.coffeeMessages = [
			{
				"username": "Coffee Situation Badger",
				"message": "Me a badger. Know not many coffee things until it's too asnake, late.", 
				"icon": ":badger:",
			},
			{
				"username": "Coffee Situation Moves",
				"message": "For a cup of coffee there, Ultimately AI dans.", 
				"icon": ":awesome_dance:",
			},
			{
				"username": "Coffee Situation Im batman",
				"message": "The coffee is darkest just before the dawn. And I promise you, the dawn is coming", 
				"icon": ":batsignal:",
			},
			{
				"username": "Coffee Situation Parrot",
				"message": "Someone mentioned coffee?", 
				"icon": ":fast_parrot:",
			},
			{
				"username": "Coffee Situation Picard",
				"message": "<https://www.youtube.com/watch?v=R2IJdfxWtPM|Tea, Earl Grey, Hot?>..", 
				"icon": ":picard_facepalm:",
			},
			{
				"username": "Coffee Situation Pepper",
				"message": ":pepperdance: ..?", 
				"icon": ":hot-coffee:",
			}
		]


	"""
	Sends the gathered payload to slack

	@param (dict) payload, [message]
	"""
	def notify(self, payload):
		
		messageData = random.choice(self.coffeeMessages)
		coffeeSituationUrl = payload["coffeeObservationImageUrl"]

		message = messageData["message"] +" <"+coffeeSituationUrl+"|Check the current coffee situation here>"
		icon = messageData["icon"]
		username = messageData["username"]
		channel = ("channel" in payload) and payload["channel"] or self.defaultChannel,

		return super().notify({
			"message": message,
			"channel": channel,
			"icon": icon,
			"username": username
		})