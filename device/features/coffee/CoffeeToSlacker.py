#!/usr/bin/env python3
"""
@author lsipii
"""
import random
from app.utils.slack.SlackPostWebhook import SlackPostWebhook

class CoffeeToSlacker(SlackPostWebhook):

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
				"message": "Badger Badger Badger Snake Coffee Badger Badger Badger.", 
				"icon_emoji": ":badger:",
			},
			{
				"username": "Coffee Situation: Moves",
				"message": "For a cup of coffee there, Ultimately AI dans.", 
				"icon_emoji": ":awesome_dance:",
			},
			{
				"username": "Coffee Situation: Im batman",
				"message": "The coffee is darkest just before the dawn. And I promise you, the dawn is coming.", 
				"icon_emoji": ":batsignal:",
			},
			{
				"username": "Coffee Situation: Pepper",
				"message": ":pepperdance: ..?", 
				"icon_emoji": ":hot-coffee:",
			},
			{
				"username": "Coffee Situation: Vader",
				"message": "Come to the dark side, we have coffee.", 
				"icon_emoji": ":darth_vader:",
			},
			{
				"username": "Coffee Situation: Brains",
				"message": "<https://www.youtube.com/watch?v=Nvipwdh_Naw|Take my money>...",
				"icon_emoji": ":zombie:",
			},
			{
				"username": "Coffee Situation: Parrot, pre-startup",
				"message": "..., ..., ..., club.",
				"icon_emoji": ":parrot_sleep:",
			},
			{
				"username": "Coffee Situation: Parrot, startup",
				"message": "Someone mentioned a coffee?", 
				"icon_emoji": ":coffee_parrot:",
			},
			{
				"username": "Coffee Situation: Parrot, startup-grad",
				"message": "Still boundless, the slice of black magicka surrounded by a tactical container.",
				"icon_emoji": ":gentleman_parrot:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <https://www.youtube.com/watch?v=vM9zKZXorI8|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <https://www.youtube.com/watch?v=J4juWTKDhNQ|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <https://imgur.com/r/turtle/|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <http://interactivepython.org/courselib/static/thinkcspy/MoreAboutIteration/RandomlyWalkingTurtles.html|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <https://www.youtube.com/watch?v=dV9KuETVF8I|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <https://imgur.com/gallery/98otF|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Turtle",
				"message": "Static, but random. Like a random turtle <https://www.hs.fi/nyt/art-2000005638640.html|link>.", 
				"icon_emoji": ":turtle:",
			},
			{
				"username": "Coffee Situation: Coffee",
				"message": "Here's a nice little boredpanda article regarding <https://www.boredpanda.com/i-draw-coffee-monsters-from-random-coffee-stains/|coffee stain monsters>.", 
				"icon_emoji": ":coffee:",
			},
			{
				"username": "Coffee Situation: Coffee",
				"message": "Here's a nice little Oxford dictionarries blog regarding <https://blog.oxforddictionaries.com/2014/09/28/coffee-list/|coffee words>.", 
				"icon_emoji": ":coffee:",
			},
			{
				"username": "Coffee Situation: Youtube links",
				"message": "Time for a <https://www.youtube.com/watch?v=rGS0OWPE7IQ|Random German Coffee Ad>.", 
				"icon_emoji": ":youtube:",
			},
			{
				"username": "Coffee Situation: Youtube links",
				"message": "Time for a <https://www.youtube.com/watch?v=auK3t0MSsCA|Parks and Recreation - Ron Swanson and the Coffee Maker>.", 
				"icon_emoji": ":youtube:",
			},
			{
				"username": "Coffee Situation: Youtube links",
				"message": "Time for a <https://www.youtube.com/watch?v=s3n3goJ2z8M|Coffee Physics>.", 
				"icon_emoji": ":youtube:",
			},
		]

	"""
	Generates the slack payload

	@param (dict) payload, [message, channel, network]
	@return (dict) messageData
	"""
	def generateResponsePayload(self, payload, requestParams):
		
		# Generate a slack response payload
		coffeeMessage = random.choice(self.coffeeMessages)
		messageData = coffeeMessage.copy()

		coffeeSituationMessage = "Check the current 4th floor coffee situation here"
		if payload["streaming"]:
			coffeeSituationMessage = "STREAM: Check the current 4th floor coffee situation here"

		messageData["message"] += "\n> <"+payload["coffeeObservationUrl"]+"|"+coffeeSituationMessage+">"
		
		# Force request channel&network
		messageData["channel"] = ("channel" in requestParams) and requestParams["channel"] or self.defaultChannel
		messageData["network"] = ("network" in requestParams) and requestParams["network"] or self.defaultNetwork

		return messageData