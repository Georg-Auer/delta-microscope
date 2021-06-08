#format SD card with balena etcher, and install the latest raspian
#create a file on the card named SSH (no file extension)
#find the ip of the raspberry, it is displayed at the first boot or found via Advanced IP Scanner (Windows) or nmap in linux
#install a X11 "X Server" on your machine, for instance VcXSrv in Windows 10, or xquartz for Mac OS X http://xquartz.macosforge.org/
#login via SSH, for instance PuTTy in Windows 10 (enable X11!)
#login with username: "pi" and password "raspberry"

#change password with raspi-config for security reasons with:
#sudo raspi-config
#expand the filesystem with: “7 Advanced Options” menu item

#the rest is automatic:
sudo apt-get -y install feh

# remove unwanted stuff
sudo apt-get purge wolfram-engine -y
#sudo apt-get purge libreoffice* -y

#upgrades..
sudo apt-get upgrade -y
sudo apt-get clean -y
sudo apt autoremove -y

#needed for python opencv-contrib-python==4.1.0.25:
#sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test

# install opencv 4.4.0.44 prerequisites on raspian buster, using preinstalled python3.7
sudo apt install libaom0 libatk-bridge2.0-0 libatk1.0-0 libatlas3-base libatspi2.0-0 libavcodec58 libavformat58 libavutil56 libbluray2 libcairo-gobject2 libcairo2 libchromaprint1 libcodec2-0.8.1 libcroco3 libdatrie1 libdrm2 libepoxy0 libfontconfig1 libgdk-pixbuf2.0-0 libgfortran5 libgme0 libgraphite2-3 libgsm1 libgtk-3-0 libharfbuzz0b libilmbase23 libjbig0 libmp3lame0 libmpg123-0 libogg0 libopenexr23 libopenjp2-7 libopenmpt0 libopus0 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpixman-1-0 librsvg2-2 libshine3 libsnappy1v5 libsoxr0 libspeex1 libssh-gcrypt-4 libswresample3 libswscale5 libthai0 libtheora0 libtiff5 libtwolame0 libva-drm2 libva-x11-2 libva2 libvdpau1 libvorbis0a libvorbisenc2 libvorbisfile3 libvpx5 libwavpack1 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwebp6 libwebpmux3 libx264-155 libx265-165 libxcb-render0 libxcb-shm0 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxinerama1 libxkbcommon0 libxrandr2 libxrender1 libxvidcore4 libzvbi0

# check if any python processes are running
pgrep -lf python

pip3 install opencv-python
# cd ~/home/pi
# mkdir projects
# cd ~projects
git clone https://github.com/Georg1986/spoc.git
#georg.auer@gmail.com
#PASSWORD
cd spoc/delta_bot

sudo apt-get install virtualenv -y
sudo apt-get install virtualenvwrapper -y

#sudo pip install virtualenv 
#sudo pip install virtualenvwrapper
#sudo pip3 uninstall virtualenv virtualenvwrapper
#sudo pip uninstall virtualenv virtualenvwrapper

mkdir ~/.virtualenvs
#to remove a dir: "rm -r ~/.virtualenvs"

#write to bashrc file
echo "# virtualenv and virtualenvwrapper" >> ~/.bashrc
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
# nano ~/.bashrc

# before creating envirnoment, go to the folder where python is "which python3"
cd /usr/bin/

#create new environment named "delta" using python3 and associate with the created directory
mkvirtualenv delta -p python3 -a ~/projects/spoc/delta_bot

# this is how venv activates environments: source venv/bin/activate

/usr/local/bin/virtualenvwrapper.sh

# environment can be removed with "rmvirtualenv delta"

#installs puredata, externals are missing..
sudo apt-get -y install puredata --fix-missing

# now you have to boot puredata, an add externals:
# Help -> finde externals -> preferences: add externals to path = YES
# hide foreign architectures: NO
# now search for the following two modules and install them, click on add to path if asked:
# comport 1.1.1 for linuxarmv7-32
# mrpeach for linuxarmv7-32

# alternative automated install?
# cd /home/pi/
# sudo mkdir Pd
# sudo mkdir Pd/externals
# cd /home/pi/Pd/externals/
#import externals here - skript breaks anyway?

#arduino:
mkdir -p ~/Applications
cd ~/Applications
wget https://downloads.arduino.cc/arduino-1.8.13-linuxarm.tar.xz
tar xvJf arduino-1.8.13-linuxarm.tar.xz
cd arduino-1.8.13/
./install.sh
rm ../arduino-1.8.13-linuxarm.tar.xz

#teensy:
cd /etc/udev/rules.d/
sudo wget https://www.pjrc.com/teensy/49-teensy.rules
cd ~
sudo mkdir Downloads
cd ~/Downloads
sudo wget https://www.pjrc.com/teensy/td_153/TeensyduinoInstall.linuxarm # compatible with arduino 1.8.13
sudo chmod 755 TeensyduinoInstall.linuxarm
./TeensyduinoInstall.linuxarm
#choose where you put the installation files in the GUI
sudo rm -rf TeensyduinoInstall.linuxarm

#cameras:
# pip3 install "picamera[array]" comes preinstalled with 2020 August raspberry os

# for a apache server based web-interface install this:
# https://elinux.org/RPi-Cam-Web-Interface#Basic_Installation
cd ~
sudo mkdir Downloads
cd ~/Downloads
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd ~/Downloads/RPi_Cam_Web_Interface/
sudo ./install.sh
# now choose a picture folder, and install
# now just go to the ip of the raspberry in any browser, it should open the web interface

# permanent git setup:
# https://git-scm.com/book/de/v2/Git-auf-dem-Server-Erstellung-eines-SSH-Public-Keys
# Generating public/private rsa key pair
ssh-keygen -o
# read out ssh key
cat ~/.ssh/id_rsa.pub
# add key on github
https://github.com/settings/keys
# now git clone, push, pull.. is available without password
git clone git@github.com:Georg-Auer/spoc.git
# the next two lines should be modified
# needed for:
# git add
# git commit .
# git push
git config --global user.email "georg.auer@gmail.com"
git config --global user.name "delta-microscope"

# python 3.8.6 install
sudo mkdir ~/Downloads
cd ~/Downloads
wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tgz
# wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
# installing python 3.8 on raspberry os
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
sudo tar zxf Python-3.8.6.tgz
# sudo tar zxf Python-3.9.0.tgz
cd Python-3.8.6
# cd Python-3.9.0
sudo ./configure --enable-optimizations

#for gui installation just use
pip3 install dearpygui

# using flask and python for controlling a robot
# instructions for setting up apache2 and wsgi_mod:
# http://terokarvinen.com/2017/write-python-3-web-apps-with-apache2-mod_wsgi-install-ubuntu-16-04-xenial-every-tiny-part-tested-separately/
# first install apache
sudo apt install apache
# for using flask with apache, mod_wsgi is needed
sudo apt install libapache2-mod-wsgi-py3
# https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/
# make sure .wsgi file exists in project directory

# edit the config file
sudo nano /etc/apache2/sites-available/000-default.conf

# killing a process
# ps -ef | grep python
# kill <PID found previously>
# or:
# kill -9 <PID found previously>

# dearpygui install via cmake
# https://github.com/hoffstadt/DearPyGui/wiki/Building-For-Contributors
# sudo apt-get install cmake -y
# sudo apt-get install libgl1-mesa-dev -y
# sudo apt-get install libglu1-mesa-dev -y
# sudo apt-get install libxrandr-dev -y
# sudo apt-get install libxinerama??
# sudo apt-get install doxygen
# sudo apt-get install libxcursor-dev
# sudo apt-get install libxi-dev
# sudo apt-get install build-essential
# sudo apt-get install python3-dev libxml2-dev libxslt-dev??

# sudo apt-get install --upgrade cmake libgl1-mesa-dev libglu1-mesa-dev libglu1-mesa-dev libxrandr-dev doxygen libxcursor-dev libxi-dev build-essential python3-dev libxml2-dev -y

# sudo mkdir ~/Downloads
# cd ~/Downloads
# git clone --recursive https://github.com/hoffstadt/DearPyGui
# git clone -b "v0.6.203" --recursive https://github.com/hoffstadt/DearPyGui
# git clone -b "v0.6.202" --recursive https://github.com/hoffstadt/DearPyGui
# new build method for 0.6.203

# edit the BuildLocalWheelLinux.sh
# -------------------------------------------------------------------------------
# mkdir -p cmake-build-local
# cd cmake-build-local
# rm -rf *
# cmake .. -DMVDIST_ONLY=True -DMVPY_VERSION=0 -DMVDPG_VERSION=local_build
# make -j3
# cd ..

# cd Distribution
# python3 BuildPythonWheel.py ../cmake-build-local/DearPyGui/core.so 0
# python3 -m ensurepip
# python3 -m pip install --upgrade pip
# python3 -m pip install twine --upgrade
# python3 -m pip install wheel
# python3 -m setup bdist_wheel --plat-name linux_armv7l --dist-dir ../dist
# -------------------------------------------------------------------------------

# chmod +x BuildLocalWheelLinux.sh 
# ./BuildLocalWheelLinux.sh 

# sudo chmod +x BuildLocalWheelRPi.sh
# ./BuildLocalWheelRPi.sh

# download visual studio code from website
# https://code.visualstudio.com/#alt-downloads
# install visual studio code
# sudo dpkg -i code_1.50.0-1602050504_armhf.deb

# the following is only for the point grey camera -------------------------------------------------------------------------

# #write the following two lines into rules.d for point grey:
# #https://answers.opencv.org/question/221305/how-to-get-pointgrey-camera-acquiring-image-data-in-python-on-raspberry-pi/

# sudo tee -a /etc/udev/rules.d/10-pointgrey.rules <<EOT
# # udev rules file for Point Grey Firefly-MV
# BUS=="usb", SYSFS{idVendor}=="1e10", SYSFS{idProduct}=="3300", GROUP="plugdev"
# EOT

# # installs libdc1394 cam driver
# # https://www.flir.com/support-center/iis/machine-vision/knowledge-base/how-do-i-use-my-camera-with-linux/
# sudo apt-get install -y libdc1394-22-dev libdc1394-22 libdc1394-utils

# # maybe:
# sudo apt install -y libv4l-dev libdc1394-22 libdc1394-22-dev v4l-utils
# # and:
# sudo apt install -y ffmpeg libavcodec-dev libavformat-dev libswscale-dev libxine2-dev libfaac-dev libmp3lame-dev mplayer

# #lists all video devices
# ls /dev/video*

# # https://pypi.org/project/acapture/
# pip install acapture

# # sudo usermod -a -G video pi

# # sudo apt-get install fswebcam
# # fswebcam -d /dev/video12 image1.jpg

# #--------------super-experimental-installation-guide-not-yet-working--------------------------------------

# #pyflycam installation!
# #at first, install FlyCapture SDK 

# #(for ARM) look into the help file/webpage
# #https://www.flir.com/support-center/iis/machine-vision/application-note/getting-started-with-flycapture-2-and-arm/

# # wget https://tinyurl.com/ty2kgax
# # mv ty2kgax flycap-sdk.tar.gz
# # tar xzvf flycap-sdk.tar.gz

# # # go into the lib folder, and 
# # cd flycapture-<version>_arm/lib

# # sudo cp libflycapture* /usr/lib
# # sudo cp pwd /usr/lib

# #sudo cp -r /home/pi/.virtualenvs/delta/bin/flycapture.2.13.3.31_armhf/lib /usr/lib


# # #cd flycapture-<version>_arm/
# # cd ..


# # sudo sh flycap2-conf

# # #install tools needed by PyCapture2
# # sudo pip install setuptools cython numpy

# # cd ~/.virtualenvs/delta/bin

# # #not sure if this link works permanetly
# # wget https://tinyurl.com/snyf68t
# # #because said homepage is very excentric, the files name will be now snyf68t
# # #therefore, rename it like this:
# # mv snyf68t flycap.tar.gz
# # #extract tar.gz files with
# # tar xzvf flycap.tar.gz
# # #now install as described in the extracted file README_Linux.txt
# # sudo python setup.py install


# openFoam install
# https://www.openfoam.com/download/install-windows-10.php
sudo wget https://sourceforge.net/projects/openfoam/files/v2006/OpenFOAM-v2006-windows10.tgz
sudo tar -xvzf  OpenFOAM-v2006-windows10.tgz -C /opt/
sudo chown -R $USER /opt/OpenFOAM
sudo apt install bison flex m4
echo "source /opt/OpenFOAM/OpenFOAM-v2006/etc/bashrc" >> ~/.bashrc
source $HOME/.bashrc

# test tutorial:
mkdir -p /mnt/c/Users/<USER>/tutorial
cd /mnt/c/Users/<USER>/tutorial
cp -ar $FOAM_TUTORIALS/incompressible/icoFoam/cavity/cavity .

# copy example from video tut
# https://www.youtube.com/watch?v=KznljrgWSvo
# cp -ar $FOAM_TUTORIALS/incompressible/icoFoam/elbow .

# https://github.com/OpenFOAM/OpenFOAM-dev/tree/master/tutorials/incompressible/simpleFoam/motorBike
# cp -ar $FOAM_TUTORIALS/incompressible/icoFoam/simpleFoam/motorBike .

cd cavity
blockMesh
icoFoam
touch cavity.foam
# open .foam with ParaView
