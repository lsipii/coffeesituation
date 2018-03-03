#
#--------------------------------------------------------------------------
# Image Setup
#--------------------------------------------------------------------------
#
# Creates Zoinks raspberry pi image, rasbian
#
FROM resin/rpi-raspbian

MAINTAINER Lassi Piironen "lspii@kapsi.fi"

LABEL lsipii.tshzoink.version=1
LABEL lsipii.tshzoink.release-date="2018-03-02"

#
#--------------------------------------------------------------------------
# Install requirements
#--------------------------------------------------------------------------
#

RUN apt-get update -yqq && \
    apt-get install -y --force-yes python3-pip wget

# Workdir
WORKDIR /usr/local/src

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
    apt-get install -y --force-yes build-essential cmake pkg-config
RUN apt-get update -yqq && \
    apt-get install -y --force-yes libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
RUN apt-get update -yqq && \
    apt-get install -y --force-yes libatlas-base-dev gfortran

#####################################
# Install numpy
#####################################
# RUN pip3 install numpy

RUN apt-get update -yqq && \
    apt-get install -y --force-yes python3-numpy

#####################################
# Install opencv
#####################################

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
	    -D BUILD_EXAMPLES=ON ..

# Revert the optimizations
RUN if [ -f /etc/dphys-swapfile ]; then \
	RUN sed -i 's/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile \
;fi

#
#--------------------------------------------------------------------------
# Install motion
#--------------------------------------------------------------------------
#
RUN apt-get update -yqq && \
    apt-get install -y --force-yes motion 

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

# Stops starting at boot, we'll start in scripts
RUN systemctl disable motion

#
#--------------------------------------------------------------------------
# Install nginx
#--------------------------------------------------------------------------
#
RUN mkdir -p /var/www/html

RUN apt-get update -yqq && \
    apt-get install -y --force-yes nginx

ADD ./docker/nginx/sites/default.conf /etc/nginx/sites-available/default.conf
ADD ./docker/nginx/404/404.jpg /var/www/html/

#
#--------------------------------------------------------------------------
# Install zoinks app
#--------------------------------------------------------------------------
#

#####################################
# Copy files
#####################################
RUN mkdir -p zoinks/app
RUN mkdir -p zoinks/configs

ADD ./app/ zoinks/app/
ADD ./configs zoinks/configs/
ADD ./zoinks.py zoinks/app/
ADD ./requirements.txt zoinks/app/

#####################################
# Install requirements
#####################################
RUN pip3 install -r zoinks/app/requirements.txt

#
#--------------------------------------------------------------------------
# Finalize, cleanup
#--------------------------------------------------------------------------
#

#####################################
# The app run command
#####################################
CMD /usr/local/src/zoinks/zoinks.py --production &