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

@TODO: Raspberry Pi setups

###### Dependencies

The dependency installations are better described in the Dockerfile

Thought, multiliner and multistepper without OpenCV support would be

1. Base requirements
```
sudo apt-get update -y && sudo apt-get install -y git python3-pip nginx motion git
```

2. Motion configs
```
sudo sed -i 's/daemon off/daemon on/g' /etc/motion/motion.conf && \
	sudo sed -i 's/stream_localhost on/stream_localhost off/g' /etc/motion/motion.conf && \
	sudo sed -i 's/stream_port 0/stream_port 8081/g' /etc/motion/motion.conf && \
	sudo sed -i 's/output_pictures on/output_pictures off/g' /etc/motion/motion.conf && \
	sudo sed -i 's/ffmpeg_output_movies on/ffmpeg_output_movies off/g' /etc/motion/motion.conf && \
	sudo sed -i 's/stream_maxrate 1/stream_maxrate 25/g' /etc/motion/motion.conf && \
	sudo sed -i 's/framerate 100/framerate 25/g' /etc/motion/motion.conf && \
	sudo sed -i 's/width 352/width 640/g' /etc/motion/motion.conf && \
	sudo sed -i 's/height 288/height 480/g' /etc/motion/motion.conf && \
	sudo sed -i 's/start_motion_daemon=no/start_motion_daemon=yes/g' /etc/default/motion && \
	sudo systemctl disable motion
```

3. Clone the repository if not yet done

```
git clone https://github.com/tamperestartuphup/tshzoinks.git 
```

4. nginx configs
```
sudo cp ./docker/nginx/sites/default.conf /etc/nginx/sites-available/default.conf && \
	sudo cp ./docker/nginx/404/404.jpg /var/www/html/
```

5. Zoinks python requirements
```
pip3 install -r zoinks/app/requirements.txt
```

###### Deployment instructions

@TODO: Rasberry Pi setups

### Who do I talk to? ###

* Project owner: @lsipii 
* Administrator for the Slack bot for the Tampere Startup Hub channels: @lsipii
* Administrator for the observation device in Tampere Startup Hub: @lsipii
* Tampere Startup Hub: http://www.startuphub.fi