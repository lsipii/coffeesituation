 # README #

DRAFT

### What is this repository for? ###

* The coffee situation bot observes the current office coffee machines situation as it is important to know the status of the coffee situation
* Version v1.1

### How do I get set up? ###

#### Summary of set 

The app consists of a rasperry pi device taking pictures and a slackbot app reporting the results. Thus there are two different setups and configurations.  

##### Common dependencies

* python3
* pip3

##### Slackbot

 
1. Clone the repo to the hosting server, where the bot will be ran

2. Copy the example configurations:

cp settings/slackbot.example.json settings/slackbot.json

3. Configure very much

* SLACK_BOT_TOKEN: The slack access key, by which the bot connects to the Slack workplace
* SLACK_BOT_MAINTAINER: Slack user ID, eg. W012A3CDE
* COFFEE_BOT_TOKEN: The access key to the coffee observation device (Raspberry Pi)
* COFFEE_BOT_URL: The public access url of the coffee bot device, eg. https://xxXXxxXXXXxx.dataplicity.io


###### Dependencies

For the slackbot hosting server the reqs are listed in the slackbot_requirements.txt file

* Install by:

pip3 install -r slackbot_requirements.txt

* Deployment instructions


##### The Rasperry Pi Observation device

###### Configurations
###### Dependencies
###### Deployment instructions

### Who do I talk to? ###

* Project owner: @lsipii 
* Administrator for the Slack bot for the Tampere Startup Hub channels: @lsipii
* Administrator for the observation device in Tampere Startup Hub: @lsipii
* Tampere Startup Hub: http://www.startuphub.fi