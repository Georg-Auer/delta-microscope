# How to set up a Raspberry 3b / 4 for use with the SPOC lab Microscope

# Download Raspberry Pi Imager and install the latest version of Raspberry OS on an SD card with at least 32 GB
# Create a file on the card named SSH (no file extension), the Raspberry can now be used "headless" over network without a display.
# https://www.raspberrypi.org/software/

# Now find the ip of the raspberry, it is displayed at the first boot (Display needed for this step)
# or found via Advanced IP Scanner (Windows) or nmap in linux
# Now install a X11 "X Server" on your machine, for instance VcXSrv https://sourceforge.net/projects/vcxsrv/ in Windows 10,
# or xquartz for Mac OS X http://xquartz.macosforge.org/
# Login via SSH, for instance PuTTy in Windows 10 or MacOS X (enable X11!)
# login with username: "pi" and password "raspberry"

# Now change password with raspi-config for security reasons with:
# sudo raspi-config
# Expand the filesystem with: “7 Advanced Options” menu item if applicable

# The rest is automatically done with this script:
sudo apt-get -y install feh

#upgrades..
sudo apt update -y
sudo apt upgrade -y

sudo apt clean -y
sudo apt autoremove -y

#installs puredata, externals are missing..
sudo apt-get -y install puredata --fix-missing

# now you have to boot puredata, an add externals:
# Help -> finde externals -> preferences: add externals to path = YES
# hide foreign architectures: NO
# now search for the following two modules and install them, click on add to path if asked:
# comport 1.1.1 for linuxarmv7-32
# mrpeach for linuxarmv7-32

# alternative automated install:
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

# now choose a picture folder, and install
# now just go to the ip of the raspberry in any browser, it should open the web interface

cd ~
git clone git@github.com:spoc-lab/delta-microscope.git

#sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test
# install opencv 4.4.0.44 prerequisites on raspian buster, using preinstalled python3.7
sudo apt install -y libaom0 libatk-bridge2.0-0 libatk1.0-0 libatlas3-base libatspi2.0-0 libavcodec58 libavformat58 libavutil56 libbluray2 libcairo-gobject2 libcairo2 libchromaprint1 libcodec2-0.8.1 libcroco3 libdatrie1 libdrm2 libepoxy0 libfontconfig1 libgdk-pixbuf2.0-0 libgfortran5 libgme0 libgraphite2-3 libgsm1 libgtk-3-0 libharfbuzz0b libilmbase23 libjbig0 libmp3lame0 libmpg123-0 libogg0 libopenexr23 libopenjp2-7 libopenmpt0 libopus0 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 libpixman-1-0 librsvg2-2 libshine3 libsnappy1v5 libsoxr0 libspeex1 libssh-gcrypt-4 libswresample3 libswscale5 libthai0 libtheora0 libtiff5 libtwolame0 libva-drm2 libva-x11-2 libva2 libvdpau1 libvorbis0a libvorbisenc2 libvorbisfile3 libvpx5 libwavpack1 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwebp6 libwebpmux3 libx264-155 libx265-165 libxcb-render0 libxcb-shm0 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxinerama1 libxkbcommon0 libxrandr2 libxrender1 libxvidcore4 libzvbi0

# the local python3 will be modified:
sudo pip3 install opencv-python

# # python 3.8.9 install
# sudo mkdir ~/Downloads
# cd ~/Downloads
# wget https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz
# # installing python 3.8 on raspberry os
# sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
# sudo tar zxf Python-3.8.9.tgz
# cd Python-3.8.9
# sudo ./configure --enable-optimizations
# make altinstall 

# # python 3.9.6 install on raspberry os
# sudo apt install -y wget build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
# sudo mkdir ~/Downloads
# cd ~/Downloads
# wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
# sudo tar zxf Python-3.9.5.tgz
# cd Python-3.9.5
# sudo ./configure --enable-optimizations
# make altinstall 

# check if any python processes are running
# pgrep -lf python
# killing a process
# ps -ef | grep python
# kill <PID found previously>
# or:
# kill -9 <PID found previously>

