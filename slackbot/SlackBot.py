# -*- coding: utf-8 -*-
"""
@author lsipii
@see https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
"""
from slackclient import SlackClient
import urllib
import json
import time

class SlackBot():

    """
    Initializes the slack client
    
    @param (AppInfo) app
    """
    def __init__(self, app):
        
        # References the app and configs
        self.app = app
        self.config = app.config

        # Validate config
        if "SLACK_BOT_TOKEN" not in self.config:
            raise Exception("SLACK_BOT_TOKEN not in slackbot config")
        if "COFFEE_BOT_TOKEN" not in self.config:
            raise Exception("COFFEE_BOT_TOKEN not in slackbot config")
        if "COFFEE_BOT_URL" not in self.config:
            raise Exception("COFFEE_BOT_URL not in slackbot config")
        if "SLACK_BOT_MAINTAINER" not in self.config:
            raise Exception("SLACK_BOT_MAINTAINER not in slackbot config")

        # Slack variables
        self.slack = SlackClient(self.config["SLACK_BOT_TOKEN"])
        self.slackBotUser = None
        self.slackRTMReadDelay = 1 # 1 sec read delay
        self.slackbotMaintainerIdentifier = self.config["SLACK_BOT_MAINTAINER"]

        # Internal flags
        self.debugMode = False
        self.commandInProgress = False

        # Coffee keywords
        self.coffeeKeywords = [
            "kahvi", 
            "kahve",
            "kohve",
            "kohvi",
            "kaffe",
            "kahavi",
            "sumppi",
            "suppii",
            "sumpe",
            "sumpit",
            "caffe",
            "coffee",
            "cafe",
            "kofe",
            "cofe",
        ]

    """
    Engages the client using Slacks Real Time Messaging websocket API
    """
    def engage(self):
        if self.slack.rtm_connect(with_team_state=False):
            
            # Configures the connection
            self.slackBotUser = self.slack.api_call("auth.test")
            
            # Validates the connection
            if not self.slackBotUser["ok"]:
                self.printDebugMessage("Slackbot authentication error", 1, True)

            self.printDebugMessage("Slack connection successful")
            self.printDebugMessage("Listening..")
            
            # The primary loop
            while True:
                if not self.commandInProgress:
                    self.resolveAndFireCommand(self.slack.rtm_read())            
                time.sleep(self.slackRTMReadDelay)
        else:
            self.printDebugMessage("Slackbot connection failed", 1, True)

    """
    Parses the slack events for commands to fire, fires commands 

    @param (array) slackEvents
    """
    def resolveAndFireCommand(self, slackEvents):

        """
        Validates the event
        
        @param (SlackEvent dict) event
        @return (bool) weWantThisEvent
        """
        def validateEvent(event):
            isValidEvent = False
            if event["type"] == "message" or event["type"] == "message.im":
                isValidEvent = True
            if isValidEvent and "subtype" in event:
                isValidEvent = False
            if isValidEvent and "user" not in event:
                isValidEvent = False
            return isValidEvent

        # Loop through the events, fire!
        for event in slackEvents:
            try:
                if validateEvent(event):
                    if self.checkForDirectBotCommand(event):
                        self.fireBotControlCommand(event)
                        break
                    elif self.checkIfShouldAskForACoffee(event["user"], event["text"]):
                        self.fireAskForCoffeeEventResponse(event)
                        break
            except Exception as e:
                self.printDebugMessage("resolveAndFireCommand exception: "+str(e))
                self.sendBotDefaultErrorMsg(event["channel"])
                break

    """
    Resolves and fires slack bot control command

    @param (SlackEvent dict) event
    """
    def fireBotControlCommand(self, event):
        message = event["text"].lower()
        channel = event["channel"]

        # Flags as in progress
        self.commandInProgress = True

        try:
            if message.find("help") > -1 or message.find("ohje") > -1:
                self.sendBotHelpResponse(channel)
            elif message.find("list") > -1:
               self.sendBotCoffeeKeywordsResponse(channel)
            elif message.find("status") > -1:
               self.fireCoffeeSituationAppStatusQueryResponse(event)
            elif message.find("joke") > -1 or message.find("vitsi") > -1:
               self.sendPyJokesResponse(channel)
            elif self.checkIfShouldAskForACoffee(event["user"], event["text"]):
                self.fireAskForCoffeeEventResponse(event)
            else:
                self.sendBotHelpResponse(channel, "Sorry, the command not recognized")
        except Exception as e:
            self.printDebugMessage("fireBotControlCommand exception: "+str(e))
            self.sendBotDefaultErrorMsg(channel)

        # Flags as not in progress
        self.commandInProgress = False

    """
    Asks for coffee

    @param (SlackEvent dict) event
    """
    def fireAskForCoffeeEventResponse(self, event):
        self.fireCoffeeCherkerAppQuery(event, self.config["COFFEE_BOT_URL"])

    """
    Asks for coffee app status

    @param (SlackEvent dict) event
    """
    def fireCoffeeSituationAppStatusQueryResponse(self, event):
        
        """
        Handles the response

        @param (Response) resp
        """
        def responseHandler(resp):
            try:
                # Parsing the response
                responseData = json.loads(resp.decode('utf-8'))

                if "status" in responseData:
                    if responseData["status"] == "OK":
                        self.sendSlackBotResponse(event["channel"], "The monitoring app is running")
                    else:
                        self.sendSlackBotResponse(event["channel"], "The monitoring app returned response status: "+responseData["status"])
                else:
                    self.sendSlackBotResponse(event["channel"], "The monitoring app did not respond")
            except Exception as e:
                self.sendSlackBotResponse(event["channel"], "The monitoring app did not respond")
             
        # Fires the query
        self.fireCoffeeCherkerAppQuery(event, self.config["COFFEE_BOT_URL"]+"/status", responseHandler)

    """
    Asks the coffee checking camera app a something
    
    @param (SlackEvent dict) event
    @param (string) apiEndPointAddr
    @param (callable) callback = None
    """
    def fireCoffeeCherkerAppQuery(self, event, apiEndPointAddr, callback = None):
        # Flags as in progress
        self.commandInProgress = True

        try:

            network = self.slackBotUser["url"].replace("https://", "").replace(".slack.com/", "")

            # Arrange request data
            data = urllib.parse.urlencode({
                'api_token': self.config["COFFEE_BOT_TOKEN"], 
                'channel': event["channel"], 
                'network': network,
                'message': event["text"],
                'username': event["user"],
                'app': self.app.getAppName(), 
                'app_version': self.app.getAppVersion()
            }).encode()

            # Make the request
            req =  urllib.request.Request(apiEndPointAddr, data=data)
            resp = urllib.request.urlopen(req).read()
        
            if callback is None:

                # Parsing the response
                responseData = json.loads(resp.decode('utf-8'))

                # Expects a notify container with a message in the response
                if "notify" in responseData and "message" in responseData["notify"]:
                    self.sendSlackBotResponse(event["channel"], responseData["notify"]["message"], responseData["notify"])
                else:
                    self.printDebugMessage("fireCoffeeCherkerAppQuery response:")
                    self.printDebugMessage(responseData)
                    self.sendBotDefaultErrorMsg(event["channel"])
            else:
                callback(resp)

        except Exception as e:
            self.printDebugMessage("fireAskForCoffeeEvent exception: "+str(e))
            self.sendBotDefaultErrorMsg(event["channel"])

        # Flags as in progress
        self.commandInProgress = False

    """
    Sends bot help text to a channel

    @param (string) channel
    @param (string) errorMsg = None
    """
    def sendBotHelpResponse(self, channel, errorMsg = None):
        helpTextLines = [
            "*Usage:*",
            "> - Help: Prints this usage text",
            "> - Status: Checks if the coffee situation monitoring device is online",
            "> - Joke: Well, why not?",
            "> - List: Prints accepted coffee related keywords",
            "> - `Coffee keyword`: Takes a photo of the current coffee situation",
            "> ",
            "> _Note: image url lasts max 2h, parts of the image are blurred_",
            "> _Maintenance: <@"+self.slackbotMaintainerIdentifier+">_"
        ]

        if errorMsg is not None:
            helpTextLines.insert(0, errorMsg)

        helpText = "\n".join(helpTextLines)
        self.sendSlackBotResponse(channel, helpText)

    """
    Sends bot help text to a channel

    @param (string) channel
    """
    def sendBotCoffeeKeywordsResponse(self, channel):
        helpText = "*Coffee keywords:*\n> "
        keywords = ", ".join(self.coffeeKeywords)
        helpText += keywords
        helpText += "\n> _Note: Keyword matching is not strict_"
        self.sendSlackBotResponse(channel, helpText)


    """
    Sends a pyjokes joke as a response

    @param (string) channel
    """
    def sendPyJokesResponse(self, channel):
        try:
            import pyjokes
            helpText = pyjokes.get_joke(category="chuck")
            self.sendSlackBotResponse(channel, helpText, {"icon_emoji":":markusman2:", "username":"Höhöhö Situation"})
        except Exception as e:
            self.sendSlackBotResponse(channel, "jokes lib not installed, out of jokes haha")

    """
    Sets the bot in debugmode

    @param (bool) debugMode
    """
    def sendBotDefaultErrorMsg(self, channel):
        helpText = "Sorry, the bot is busy solving a random encounter"
        self.sendSlackBotResponse(channel, helpText)

    """
    Sends a bot response back to the channel

    @param (string) channel
    @param (string) responseText
    @param (dict) slackResponseData = None, {icon_emoji|icon_url, username, unfurl_media, unfurl_links}
    """
    def sendSlackBotResponse(self, channel, responseText, slackResponseData = None):

        newLinesList = responseText.split('\n')
        responseTextFallback = ', '.join(newLinesList)
        responseTextFallback = responseTextFallback.replace(':, ', ': ')

        postArgs = {
            "channel": channel,
            "attachments": [{
                "text": responseText,
                "fallback": responseTextFallback,
                "color": "#452d19",
            }],
            "unfurl_media": False,
            "unfurl_links": False,
        }

        if slackResponseData is not None:
            if "icon_emoji" in slackResponseData:
                postArgs["icon_emoji"] = slackResponseData["icon_emoji"]
            elif "icon_url" in slackResponseData:
                postArgs["icon_url"] = slackResponseData["icon_url"]
            if "username" in slackResponseData:
                postArgs["username"] = slackResponseData["username"]
            if "unfurl_media" in slackResponseData:
                postArgs["unfurl_media"] = slackResponseData["unfurl_media"]
            if "unfurl_links" in slackResponseData:
                postArgs["unfurl_links"] = slackResponseData["unfurl_links"]

        self.slack.api_call("chat.postMessage", **postArgs)

    """
    Checks for bot control commands

    @param (SlackEvent dict) event
    @return (bool) weShouldIndeed
    """    
    def checkForDirectBotCommand(self, event):
        if event["user"] != self.slackBotUser["user_id"]:
            if self.checkIfDirectBotMessageEvent(event):
                return True
            else:
                return event["text"].find("<@"+self.slackBotUser["user_id"]+">") > -1
        return False

    """
    Checks if coffee was asked, fires the asker if so

    @param (string) slackUserId
    @param (string) message
    @return (bool) weShouldIndeed
    """
    def checkIfShouldAskForACoffee(self, slackUserId, message):

        # we should indeed
        weShouldIndeed = False

        # Sanitize the message
        lowerCaseMessage = message.lower()
        lowerCaseMessage = lowerCaseMessage.replace('é', 'e')
        lowerCaseMessageParts = lowerCaseMessage.split(" ")

        # Check for any matches
        for keyWord in lowerCaseMessageParts:
            # Skip keywords starting with # or @
            if not keyWord.startswith("#coffeesituation") and not keyWord.startswith("@Coffee"):
                for coffeeKeyword in self.coffeeKeywords:
                    if coffeeKeyword in keyWord:
                        weShouldIndeed = True
                        break
            if weShouldIndeed:
                break

        # If a match, validate the user
        if weShouldIndeed:
            user = self.getSlackUser(slackUserId)
            if user is False:
                return False
            elif user["name"].startswith("Coffee_Situation:"): 
                return False

        return weShouldIndeed


    """
    Checks if the message was sent to an public channel

    @param (SlackEvent dict) event
    @return (bool) isADirectBotQueryEvent
    """
    def checkIfDirectBotMessageEvent(self, event):
        
        if event["type"] == "message.im":
            return True

        # Ask from the API
        resp = self.slack.api_call(
            "channels.info",
            channel=event["channel"]
        )

        if "ok" in resp and not resp["ok"]:
            return True
        return False

    """
    Gets slack user info by ID

    @param (string) slackUserId
    @return (SlackUser dict|bool) user
    """
    def getSlackUser(self, slackUserId):
        resp = self.slack.api_call(
            "users.info",
            user=slackUserId
        )
        if "ok" in resp and resp["ok"]:
            return resp["user"]
        return False

    """
    Sets the bot in debugmode

    @param (bool) debugMode
    """
    def setDebugMode(self, debugMode):
        self.debugMode = debugMode

    """
    Prints a debug message in the runner console
    
    @param (string) message
    @param (int) exitCode = None, exits in debug mode if set
    @param (bool) exitAnyHow = False, disregards the debug mode
    """
    def printDebugMessage(self, message, exitCode = None, exitAnyHow = False):
        if self.debugMode:
            print(message)
            if exitCode is not None:
                exit(exitCode)
        elif exitAnyHow and exitCode is not None:
            print(message)
            exit(exitCode)