#!/usr/bin/env python3
"""
@author lsipii
"""
import random
from app.utils.Slack import Slack

class CoffeeToSlacker(Slack):

	"""
	Slack messanger, coffee overrides

	@param (dict) configs
	"""
	def __init__(self, configs):
		super().__init__(configs)

		# Some defaults
		self.defaultChannel = "#tests"
		self.defaultNetwork = "irc.aarium"

		# Define coffee messages
		self.coffeeMessages = [
			{
				"username": "Coffee Situation: Badger",
				"message": "Me a badger. Know not many coffee things until it's too asnake, late.", 
				"icon": ":badger:",
			},
			{
				"username": "Coffee Situation: Moves",
				"message": "For a cup of coffee there, Ultimately AI dans.", 
				"icon": ":awesome_dance:",
			},
			{
				"username": "Coffee Situation: Im batman",
				"message": "The coffee is darkest just before the dawn. And I promise you, the dawn is coming", 
				"icon": ":batsignal:",
			},
			{
				"username": "Coffee Situation: Picard",
				"message": "<https://www.youtube.com/watch?v=R2IJdfxWtPM|Tea, Earl Grey, Hot?>..", 
				"icon": ":picard_facepalm:",
			},
			{
				"username": "Coffee Situation: Pepper",
				"message": ":pepperdance: ..?", 
				"icon": ":hot-coffee:",
			},
			{
				"username": "Coffee Situation: Vader",
				"message": "Come to the dark side, we have coffee", 
				"icon": ":darth_vader:",
			},
			{
				"username": "Coffee Situation: Brains",
				"message": "<https://www.youtube.com/watch?v=Nvipwdh_Naw|Take all my money>",
				"icon": ":zombie:",
			},
			{
				"username": "Coffee Situation: Parrot, pre-startup",
				"message": "..., ..., ..., club",
				"icon": ":parrot_sleep:",
			},
			{
				"username": "Coffee Situation: Parrot, startup",
				"message": "Someone mentioned a coffee?", 
				"icon": ":coffee_parrot:",
			},
			{
				"username": "Coffee Situation: Parrot, startup-grad",
				"message": "Boundless, the slice of black magicka surrounded by a tactical container",
				"icon": ":gentleman_parrot:",
			}
		]


	"""
	Gathers some payload for slack, sends
	
	@param (dict) payload, [message]
	@param (dict) payload, [channel, network]
	@return (response)
	"""
	def notifyCoffeeRequest(self, payload, requestParams):
		# Force request channel&network
		if "channel" in requestParams:
			payload["channel"] = requestParams["channel"]
		if "network" in requestParams:
			payload["network"] = requestParams["network"]
		return self.notify(payload)

	"""
	Sends the gathered payload to slack

	@param (dict) payload, [message, channel, network]
	@return (response)
	"""
	def notify(self, payload):
		
		messageData = random.choice(self.coffeeMessages)
		coffeeSituationUrl = payload["coffeeObservationImageUrl"]

		message = messageData["message"] +" <"+coffeeSituationUrl+"|Check the current coffee situation here>"
		icon = messageData["icon"]
		username = messageData["username"]
		channel = ("channel" in payload) and payload["channel"] or self.defaultChannel
		network = ("network" in payload) and payload["network"] or self.defaultNetwork

		return super().notify({
			"message": message,
			"channel": channel,
			"network": network,
			"icon": icon,
			"username": username
		})