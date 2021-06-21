# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:23:40 2019

@author: Georg Auer
"""

# Starts OSC, Initializes connection to localhost
# Documentation can be found here
# https://buildmedia.readthedocs.org/media/pdf/osc4py3/latest/osc4py3.pdf
# https://osc4py3.readthedocs.io/en/latest/userdoc.html#sending-messages
# Question remains: Is osc4py3.as_eventloop perfect for such a usage

# Import needed modules from osc4py3 (instead of * as in tutorial)
from osc4py3.as_eventloop import osc_udp_client, osc_startup, osc_send, osc_process, osc_terminate
from osc4py3 import oscbuildparse
import time

# Teensy should accept coordinates, and give back coordinates.
# saving of images would be more useful this way, and navigating back to a ROI would be possible
# import numpy as np

class Position:
    # Initializer / Instance Attributes
    def __init__(self, name, x_coordinate, y_coordinate, z_coordinate, picture = 0):
        self.name = name
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.picture = picture

    def description(self):
        if((self.picture) != 0):
            print(f"Position: {self.name}, ")
            print(f"Picture taken at coordinates: x = {self.x_coordinate} y = {self.y_coordinate} z = {self.z_coordinate} ")
            print(f"Filename: {self.picture}")
        else:
            print(f"Position: {self.name}, ")
            print(f"No picture taken at coordinates: x = {self.x_coordinate} y = {self.y_coordinate} z = {self.z_coordinate} ")

    def picture_name(self):
        if((self.picture) != 0):
            return self.picture

    def osc_message(self):
        print(f"Moving to coordinates: x = {self.x_coordinate} y = {self.y_coordinate} z = {self.z_coordinate} ")
        exectime = time.time() + 10   # execute in 10 seconds
        print(self.x_coordinate, self.y_coordinate, self.z_coordinate) #to see what is sent
        msg1 = oscbuildparse.OSCMessage("/oscControl/slider3Dx", None, [self.x_coordinate])
        msg2 = oscbuildparse.OSCMessage("/oscControl/slider3Dy", None, [self.y_coordinate])
        msg3 = oscbuildparse.OSCMessage("/oscControl/slider3Dz", None, [self.z_coordinate])
        bun = oscbuildparse.OSCBundle(oscbuildparse.unixtime2timetag(exectime),
                            [msg1, msg2, msg3])
        return bun

    def take_picture_at_position(img_counter):
        import cv2
        cam = cv2.VideoCapture(0) #0 is the first usb webcam
        ret, frame = cam.read()
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        cam.release()
        cv2.destroyAllWindows()

def homeing():
    print("Homing in process")
    msg = oscbuildparse.OSCMessage("/oscControl/homeing", None, [2])
    return msg

def fullautomation_purrdata(active):
    if (active == 1):
        print("Activating Auto Mode")
        msg = oscbuildparse.OSCMessage("/oscControl/fullautomation", None, [1])
    else:
        print("Deactivating Auto Mode")
        msg = oscbuildparse.OSCMessage("/oscControl/fullautomation", None, [0])
    return msg

#OSC-sending-part, this also starts and ends communication:
def send_osc(msg_to_be_sent):
    #---------------------------------------------------------
    ip = "127.0.0.1"
    osc_startup()
    osc_udp_client(ip, 3001, "localhost")
    #---------------------------------------------------------

    msg = msg_to_be_sent

    #---------------------------------------------------------
    osc_send(msg, "localhost")
    #This starts the osc process, executes once
    osc_process()
    #---------------------------------------------------------
    # This terminates the osc process
    osc_terminate()

# def save_position(x,y,z):

# def take_picture_at_position(x,y,z):


# p1 = Position("pic1", 100000, 100000, 375000)
# p2 = Position(-100000, -100000, 375000)

# for p in Position._registry:
#     print (p.description())
#     time.sleep(2)

# print(p2.osc_message())

# send_osc(homeing())
# send_osc(p2.osc_message())
