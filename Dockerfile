#
#--------------------------------------------------------------------------
# Image Setup
#--------------------------------------------------------------------------
#
# Coffee situation Raspberry Pi resin.io image 
#
# Image tag: lsipii/coffeesituation
# Image version tags: https://hub.docker.com/r/lsipii/coffeesituation/tags/
# Image Github repository: https://github.com/lsipii/coffeesituation
#

FROM resin/rpi-raspbian
#FROM debian:stretch

LABEL maintainer="lspii@kapsi.fi"

#
#--------------------------------------------------------------------------
# Install requirements
#--------------------------------------------------------------------------
#

RUN apt-get update -yqq && \
    apt-get install -y python3-pip wget sudo

#
#--------------------------------------------------------------------------
# Install opencv and numpy
# @see: https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
#--------------------------------------------------------------------------
#

# OpenCV version 
ENV OPENCV_VERSION 3.4.1

#####################################
# Install requirements
#####################################

RUN apt-get update -yqq && \
    apt-get install -y build-essential cmake pkg-config
RUN apt-get update -yqq && \
    apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
RUN apt-get update -yqq && \
    apt-get install -y libatlas-base-dev gfortran
RUN apt-get update -yqq && \
    apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt-get update -yqq && \
    apt-get install -y libxvidcore-dev libx264-dev


#####################################
# Install numpy and python opencv bindings
#####################################
# ALT install method:
#
# RUN pip3 install numpy
# RUN pip3 install python-opencv

RUN apt-get update -yqq && \
    apt-get install -y python3-numpy python-opencv

#####################################
# Install opencv
#####################################

# Create a build dir
RUN mkdir -p /opencv
WORKDIR /opencv

RUN wget -q -O opencv.tar.gz https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz && \
	tar -xzf opencv.tar.gz && \
	rm opencv.tar.gz

# Optimizations for compiling
RUN if [ -f /etc/dphys-swapfile ]; then \
	sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=1024/g' /etc/dphys-swapfile \
;fi

RUN cd opencv-${OPENCV_VERSION} && \
	mkdir -p build && \
	cd build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
	    -D CMAKE_INSTALL_PREFIX=/usr/local \
	    -D INSTALL_PYTHON_EXAMPLES=ON \
	    -D BUILD_EXAMPLES=ON .. && \
	make -j4 && \
	make install && \
	ldconfig

# Revert the optimizations
RUN if [ -f /etc/dphys-swapfile ]; then \
	RUN sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile \
;fi

# Cleanup
WORKDIR /
RUN rm -rf /opencv

#
#--------------------------------------------------------------------------
# Install motion
#--------------------------------------------------------------------------
#
RUN apt-get update -yqq && \
    apt-get install -y motion 

RUN sed -i 's/daemon off/daemon on/g' /etc/motion/motion.conf && \
	sed -i 's/stream_localhost on/stream_localhost off/g' /etc/motion/motion.conf && \
	sed -i 's/stream_port 0/stream_port 8081/g' /etc/motion/motion.conf && \
	sed -i 's/output_pictures on/output_pictures off/g' /etc/motion/motion.conf && \
	sed -i 's/ffmpeg_output_movies on/ffmpeg_output_movies off/g' /etc/motion/motion.conf && \
	sed -i 's/stream_maxrate 1/stream_maxrate 25/g' /etc/motion/motion.conf && \
	sed -i 's/framerate 100/framerate 25/g' /etc/motion/motion.conf && \
	sed -i 's/width 352/width 640/g' /etc/motion/motion.conf && \
	sed -i 's/height 288/height 480/g' /etc/motion/motion.conf

RUN sed -i 's/start_motion_daemon=no/start_motion_daemon=yes/g' /etc/default/motion

# Stops starting at boot, we'll start it in the scripts
RUN systemctl disable motion

#
#--------------------------------------------------------------------------
# Install nginx
#--------------------------------------------------------------------------
#
RUN mkdir -p /var/www/html

RUN apt-get update -yqq && \
    apt-get install -y nginx

COPY ./docker/nginx/sites/default.conf /etc/nginx/sites-available/default
COPY ./docker/nginx/404/404.jpg /var/www/html/

#
#--------------------------------------------------------------------------
# Install the coffeesituation app
#--------------------------------------------------------------------------
#

ENV COFFEE_SITUATION_APP_PATH /usr/local/src/coffeesituation

#####################################
# Copy app files
#####################################

RUN mkdir -p ${COFFEE_SITUATION_APP_PATH}/device
RUN mkdir -p ${COFFEE_SITUATION_APP_PATH}/config
RUN mkdir -p ${COFFEE_SITUATION_APP_PATH}/apps/DeviceApp

COPY ./apps/DeviceApp/ ${COFFEE_SITUATION_APP_PATH}/apps/DeviceApp/
COPY ./config ${COFFEE_SITUATION_APP_PATH}/config/
COPY ./deviceApp.py ${COFFEE_SITUATION_APP_PATH}/
COPY ./requirements.txt ${COFFEE_SITUATION_APP_PATH}/

#####################################
# Install the app requirements
#####################################
RUN pip3 install -r ${COFFEE_SITUATION_APP_PATH}/requirements.txt

#####################################
# Crontab
#####################################

COPY ./docker/crontab /etc/cron.d

RUN chmod -R 644 /etc/cron.d

#
#--------------------------------------------------------------------------
# Finalize, cleanup
#--------------------------------------------------------------------------
#

# Workdir
WORKDIR ${COFFEE_SITUATION_APP_PATH}

#####################################
# The app run command
#####################################
CMD ${COFFEE_SITUATION_APP_PATH}/deviceApp.py --production &
