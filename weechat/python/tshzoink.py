# -*- coding: utf-8 -*-
"""
@author lsipii
# Derived from: irssinotifier
"""
import weechat
import urllib

weechat.register("tshzoink", "TshZoink", "1.0", "GPL3", "Responds to coffee queries", "", "")
weechat.prnt("", "TSH Zoink registered")

# Settings
settings = {
    "api_token": "",
}

for option, default_value in settings.items():
    if weechat.config_get_plugin(option) == "":
        weechat.prnt("", weechat.prefix("error") + "tshzoink: Please set option: %s" % option)
        weechat.prnt("", "tshzoink: /set plugins.var.python.tshzoink.%s STRING" % option)

# Hook message listener
weechat.hook_print("", "", "", 1, "checkIfShouldAskForACoffee", "")

"""
Checks if coffee was asked, fires the asker if so
"""
def checkIfShouldAskForACoffee(data, bufferp, uber_empty, tagsn, isdisplayed, ishilight, prefix, message):

    # Validate message sender
    if prefix is not None and prefix.startswith("Coffee_Situation:"):
        return weechat.WEECHAT_RC_OK

    # Accepted networks and thus channels
    acceptedCoffeeNetworks = [
        {
            "network": "irc.aarium", 
            "channels": ["#tests","#tests2"], 
        },
        {
            "network": "irc.tamperestartuphub",
            "channels": ["#random"], 
        }
    ]

    #@disabled: check for specific coffee sentences
    #coffeeQuestions = ["Onkohan kahvia", "coffee can I has"]
    
    #@enabled: Allowed coffee keywords
    coffeeKeywords = [
        "kahvi", 
        "kahvii", 
        "kahvetta",
        "kohvetta",
        "kaffe",
        "kahavia",
        "sumppi",
        "sumpetta",
        "sumpit",
        "caffe",
        "coffee",
        "cafe",
        "café", 
        "kofeiini",
    ]
    
    # Resolve the accepted network
    bufferBullName = weechat.buffer_get_string(bufferp, "full_name")
    acceptedNetwork = False

    for network in acceptedCoffeeNetworks:
        networkName = network["network"]
        if bufferBullName.startswith(networkName+"."):
            acceptedNetwork = network
            break

    if acceptedNetwork is not False:
        
        # Resolve the networks channel
        channel = (weechat.buffer_get_string(bufferp, "short_name") or weechat.buffer_get_string(bufferp, "name"))
        accpetedChannels = acceptedNetwork["channels"]

        # If in accepted chans, run the coffee asking query
        if channel in accpetedChannels:

            # Makes the check caseinsensitive
            lowerCaseMessage = message.lower()

            #@disabled: check for specific sentences
            #if message in coffeeQuestions:

            #@enabled: check for specific keywords
            if any(keyWord in lowerCaseMessage for keyWord in coffeeKeywords):
                askForCoffee(channel, acceptedNetwork["network"], prefix, message)

    return weechat.WEECHAT_RC_OK

"""
Asks for coffee

@param (string) channel
@param (string) network
@param (string) username
@param (string) message
"""
def askForCoffee(channel, network, username, message):
    API_TOKEN = weechat.config_get_plugin("api_token")
    if API_TOKEN != "":
        url = "https://morphotic-cow-5470.dataplicity.io/"
        postdata = urllib.urlencode({
            'api_token':API_TOKEN, 
            'channel': channel, 
            'network': network,
            'message': message,
            'username': username,
            'app':'weechat', 
            'app_version':1
        })
        hook1 = weechat.hook_process_hashtable("url:"+url, {"postfields":  postdata}, 6000, "", "")
