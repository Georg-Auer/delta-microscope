# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 10:23:40 2019

@author: Georg Auer
"""
# Starts OSC, Initializes connection to localhost
# Documentation can be found here
# https://buildmedia.readthedocs.org/media/pdf/osc4py3/latest/osc4py3.pdf
# https://osc4py3.readthedocs.io/en/latest/userdoc.html#sending-messages
# Question remains: Is osc4py3.as_eventloop perfect for such a usage?

# programs used: Python 3.6.9, Pd-l2ork-2.9.0
# FlyCap2 2.13.3.61 driver and respective PyCapture2
# following files where used: 
# calibration.py (this python code)
# movement.py, position.py and camera.py are needed for this script to work
# 191021_delta_module_cam_trigger_endstops.pd, this is dependent on the file o.io.slipserial.pd
# 191029_delta_module_OSC_Receiver-Georg.pd

# Import needed modules from osc4py3
from osc4py3.as_eventloop import osc_udp_client, \
    osc_startup, osc_send, osc_process, osc_terminate
from osc4py3 import oscbuildparse
import time

# Import self made picture taking script and movement functions:
from position_osc import Position
from position_osc import send_osc
from position_osc import homeing

#new python communication-------------------------------------------------------------
#from position_osc import Position

import numpy as np

# Set working directory
# import os
# os.chdir(r'C:\Users\Georg\Documents\Python Scripts\delta_bot\calibration')
# import PyCapture2

import cv2

# this could be improved in automatically searching for cameras!
# from camera import take_raspicampic as take_picture
# from camera import take_micropic as take_picture
# from camera import take_webcampic as take_picture

try:
    from picamera.array import PiRGBArray
    from camera import take_raspicampic as take_picture
except:
    print("Raspberry camera could not be loaded.")
    print("Trying to load webcam instead..")
    from camera import take_webcampic as take_picture

from find_intersection import find_intersection_point
from compare_intersections import compare_found_coordinates
from compare_intersections import plot_precision

def calibration_pictures(border = 1000, iterations = 1, positioning_time = 0.8, homing_time = 1):
    z = 0 # z value where object should be in focus
    #border = 100000 # value the microscope should move to each side
    #positioning_time = 9 # time it takes to move (9)
    #homing_time = 30 # time it takes to move (30)
    pictime = 0.3 # time it takes to take one picture
    time_between_iterations = 0 #this could be used for experiments

    #up_down_z = -10000
    i = 0
    calibrations = []
    while (i < iterations):
        # calibrations.append(Position("cnorm", 0, 0, z))
        # calibrations.append(Position("cdown", 0, 0, z+up_down_z))
        calibrations.append(Position("c0", 0, 0, z))
        calibrations.append(Position("c1", border, border, z))

        # calibrations.append(Position("cnorm", 0, 0, z))
        # calibrations.append(Position("cdown", 0, 0, z+up_down_z))
        calibrations.append(Position("c0", 0, 0, z))
        calibrations.append(Position("c2", border, -border, z))

        # calibrations.append(Position("cnorm", 0, 0, z))
        # calibrations.append(Position("cdown", 0, 0, z+up_down_z))
        calibrations.append(Position("c0", 0, 0, z))
        calibrations.append(Position("c3", -border, -border, z))

        # calibrations.append(Position("cnorm", 0, 0, z))
        # calibrations.append(Position("cdown", 0, 0, z+up_down_z))
        calibrations.append(Position("c0", 0, 0, z))
        calibrations.append(Position("c4", -border, border, z))

        i += 1

    #send_osc(homeing())
    #time.sleep(homing_time)
    send_osc(calibrations[0].osc_message())
    time.sleep(homing_time)

    for index, element in enumerate(calibrations):
        send_osc(element.osc_message())
        time.sleep(positioning_time)
        if element.name == 'c0':
            filename = take_picture(index)
            time.sleep(pictime)
            element.picture = filename
            print(f"Filename: {filename}")
        print("Picture taken?")
        print(element.description())

    #i += 1
    #time.sleep(time_between_iterations)
    return calibrations

def analyze_and_calibrate(iterations):
    # do calibration and get array
    calibrations = calibration_pictures(10000, iterations)
    # for each c0 picture, compare_intersections
    #print(calibrations[1].name)
    #print(calibrations[0].picture)
    zero_pos_calibration_points = []
    for element in calibrations:
        if element.name == 'c0':
            print("c0 pos found")
            #append list
            zero_pos_calibration_points = np.append(zero_pos_calibration_points, element.picture)
            print(zero_pos_calibration_points)
    coordinates = compare_found_coordinates(zero_pos_calibration_points)
    print("Standard Deviation")
    print(np.std(coordinates, axis=0))
    print("Variance")
    print(np.var(coordinates, axis=0))
    # print("Variance axis=1")
    # print(np.var(coordinates, axis=1))
    plot_precision(coordinates)

#analyze_and_calibrate(1)

def pictures_at_positions(experiment_positions, iterations = 1, positioning_time = 9, time_between_iterations = 0):
    # positioning_time = time it takes to move (9)
    # time_between_iterations = this could be increased for experiments with timepoints

    pictime = 1 # time it takes to take one picture
    i = 0
    print(iterations)
    print(i)
    while (i < iterations):

        for index, element in enumerate(experiment_positions):
            send_osc(element.osc_message())
            time.sleep(positioning_time)

            filename = take_picture(index)
            time.sleep(pictime)
            element.picture = filename
            print(f"Filename: {filename}")
            print("Picture taken?")
            print(element.description())
        i += 1
        time.sleep(time_between_iterations)

def variance_of_laplacian(image):
	# First compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
    # Suggestion: Use Gaussian Blur before Laplacien.
	return cv2.Laplacian(image, cv2.CV_64F).var()

#still needs osc movement

def autofocus(x, y, z, iterations, stepsize = 1000):
    # A maximum lap value is desired, a z position to that should be stored
    # This needs to be optimized, maybe hill climbing works well here?
    # https://www.geeksforgeeks.org/introduction-hill-climbing-artificial-intelligence/
    
    # laplacian_old = 10 # Just a starting value
    # laplacian_new = 20000 # Another(!) starting value
    direction = 1 # This value is given to movement, 0 = down, 1 = up
    number = 0 # The picture number, this increases each time a new picture is taken   
    filename = take_picture(number) #gives the number to take to takepic, gets filename back
    # This is converting the pic to grey for  analysis
    image = cv2.imread(filename) # Add ",0" to load pic in gray, if the picture is colored
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Alternatively, convert to grey
    # a first laplacian is calculated to have a value to compare against
    laplacian_old = variance_of_laplacian(image) # This gives back a value that lies mostly between 0 and 10000
    focus_stack = np.array([[z, laplacian_old]])

    # A recursive "solution" to find a high laplacian value
    while(number <= iterations):

        # sending messages needs to be put in seperate method
        # this block nevertheless moves to the first position and takes a picture
        print("Moving to coordinates: x = {} y = {} z = {} ".format(x, y, z))
        exectime = time.time() + 10   # execute in 10 seconds
        msg1 = oscbuildparse.OSCMessage("/oscControl/slider3Dx", None, [x])
        msg2 = oscbuildparse.OSCMessage("/oscControl/slider3Dy", None, [y])
        msg3 = oscbuildparse.OSCMessage("/oscControl/slider3Dz", None, [z])
        bun = oscbuildparse.OSCBundle(oscbuildparse.unixtime2timetag(exectime),
                            [msg1, msg2, msg3])
        send_osc(bun)
        # end of sending the message-----------------------------------
        #wait for movement, this should instead be an answer from arduino!
        time.sleep(2)

        filename = take_picture(number) #take a picture, store the filename
        image = cv2.imread(filename) #,0 to load pic in gray, if neccessary
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_new = variance_of_laplacian(image)

        # This writes the calculated Laplacian on the loaded image
        text = "Laplacian"
        cv2.putText(image, "{}: {:.2f}".format(text, laplacian_new), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imwrite(filename, image)

        print("New laplacian at position: ")
        print(z)
        print(laplacian_new)

        print("Old laplacian was: ")
        print(laplacian_old)
        if laplacian_old >= laplacian_new:
            direction^=True #if laplacian_old is bigger than laplacian_new, change direction
            print("Lower value, reverting direction")
        else:
            print("Higher value, moving further")

        new_z_and_laplacian = np.array([[z, laplacian_new]])
        focus_stack = np.append(focus_stack, new_z_and_laplacian, axis=0)

        if direction:
            z -= stepsize
        else:
            z += 2*stepsize
        laplacian_old = laplacian_new
        number += 1
    np.set_printoptions(precision=3)
    np.set_printoptions(suppress=True)
    # print(focus_stack)
    z_for_max_laplacian = np.argmax(focus_stack, axis=0)
    # print(z_for_max_laplacian)
    z_row = z_for_max_laplacian[1]
    # print(z_row)
    z_value = focus_stack[z_row, 0]
    z_value = int(z_value)
    # print(z_value)
    return z_value

