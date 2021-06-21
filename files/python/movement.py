"""
calibration.py (this python code)
movement.py, position.py and camera.py are needed for this script to work
@author: Georg Auer
"""

import time
import pygame
# import os
# take_webcampic can be switched to take_micropic or a different camera function
#from picamera.array import PiRGBArray
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
    from camera import take_raspicampic as take_picture
    print ("Raspicam is connected..")
except:
    print("Raspberry camera could not be loaded.")
    print("Trying to load webcam instead..")
    from camera import take_webcampic as take_picture

# from camera import take_raspicampic as take_picture
# from camera import take_micropic as take_picture 
# this also needs to import PyCapture2
# from camera import take_webcampic as take_picture

from calibration import autofocus
# import the position class from position.py
#from position import Position
from position_osc import Position

#import new method pyserialtransfer
#from position import Position
from calibration import pictures_at_positions
from calibration import calibration_pictures
from calibration import analyze_and_calibrate

import numpy as np

import cv2

# set the program icon to ico-delta.png
# os.chdir(r'C:\Users\Georg\Documents\Python Scripts\delta_bot')
# logo = pygame.image.load(os.path.join('images','ico-delta.png'))
from pathlib import Path

# test_folder = '..\microscope\images\ico-delta.png'
# logo = pygame.image.load(test_folder)
# logo = pygame.image.load('..\microscope\images\ico-delta.png')
image_folder = Path("../microscope/images/")
file_to_open = image_folder / "ico-delta.png"

# https://www.reddit.com/r/learnpython/comments/ao9tjo/using_pathlib_with_pygameimageload/
# print('Folder:')
# print(repr(test_folder))
# print(repr(file_to_open))
# if (test_folder == str(file_to_open)):
#     print('folder exactly the same')
# else: print('folder not equal')
logo = pygame.image.load(str(file_to_open))

pygame.display.set_icon(logo)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# multiplikator, to send the right values to osc..
multipl = 100

class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """

    # -- Methods
    def __init__(self, x, y, z, filename):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        # self.image = pygame.Surface([15, 15])
        # self.image.fill(BLACK)

        '''now an image is loaded for pos'''
        # self.image = pygame.image.load(filename).convert()
        # print("Folder:")
        # print(image_folder)

        # file_to_open = image_folder / filename
        # print("File to open:")
        # print(file_to_open)
        # this worked:
        # self.image = pygame.image.load(str(filename)).convert()

        file_to_open = image_folder / filename
        self.image = pygame.image.load(str(file_to_open)).convert()

        print(f"Player png loaded: {filename}{file_to_open}")

        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        self.image.set_colorkey(BLACK)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        '''z_coordinate'''
        self.z = z

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.change_z = 0

    def changespeed(self, x, y, z):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y
        self.change_z += z

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.z += self.change_z

class Marker(pygame.sprite.Sprite):
    '''
    Spawn an marker
    '''
    def __init__(self,x,y,filename):
        pygame.sprite.Sprite.__init__(self)

        '''now an image is loaded for pos'''
        # self.image = pygame.image.load(filename).convert()
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.

        # self.image = pygame.image.load(os.path.join('images',filename)).convert()
        file_to_open = image_folder / filename
        self.image = pygame.image.load(str(file_to_open)).convert()

        print(f"Marker png loaded: {filename}{file_to_open}")

        self.image.set_colorkey(BLACK)
        # self.image.convert_alpha()
        # self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()

        # self.image = pygame.image.load(filename).convert()
        # Set background color to be transparent. Adjust to WHITE if your
        # background is WHITE.
        # self.image.set_colorkey(BLACK)

        self.rect.x = x
        self.rect.y = y

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 600x600 sized screen
screen = pygame.display.set_mode([600, 600])

file_to_open = image_folder / 'background_01.png'
backdrop = pygame.image.load(str(file_to_open))
# backdrop = pygame.image.load(os.path.join('images','background_01.png')).convert()
backdropbox = screen.get_rect()

# Set the title of the window
pygame.display.set_caption('SPOC microscope prototype')

# Create the player object
# player = Player(50, 50)
# create a player object with an image
# player = Player(50, 50, 375000, os.path.join('images','liveframe.png')) # old version
player_startpos_x = 50
player_startpos_y = 50
player_startpos_z = 0
player = Player(player_startpos_x, player_startpos_y, player_startpos_z, 'liveframe.png')
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

# os.chdir(r'C:\Users\Georg\Documents\Python Scripts\delta_bot\calibration')

clock = pygame.time.Clock()
done = False
# this is only the cursor movement speed
movement_speed = 10
position_number = 0
experiment_positions = []

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-movement_speed, 0, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(movement_speed, 0, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -movement_speed, 0)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, movement_speed, 0)
            elif event.key == pygame.K_t:
                player.changespeed(0, 0, -movement_speed)
            elif event.key == pygame.K_g:
                player.changespeed(0, 0 ,movement_speed)

        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(movement_speed, 0, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-movement_speed, 0, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, movement_speed, 0)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -movement_speed, 0)
            #moving up and down, but without a send it is pretty useless atm
            elif event.key == pygame.K_t:
                player.changespeed(0, 0, movement_speed)
            elif event.key == pygame.K_g:
                player.changespeed(0, 0 ,-movement_speed)
            #take picture on spacebar release
            elif event.key == pygame.K_SPACE:

                print(f"x,y,z positions are: {player.rect.x*multipl}{player.rect.y*multipl}{player.z}")
                # take a picture and store the filename
                filename = take_picture(position_number)
                print(f"Picture taken, picture name: {filename}")
                # the new objects should be included into an array
                # new_position = Position(filename, player.rect.x, player.rect.y, player.z)
                experiment_positions.append(Position(filename, player.rect.x*multipl, player.rect.y*multipl, player.z))
                # send_osc(element.osc_message()) #which position gets sent? movement time?
                print(f"Saved as position: {position_number}")
                position_number += 1
                # os.chdir(r'C:\Users\Georg\Documents\Python Scripts\delta_bot')
                # marker = Marker(player.rect.x,player.rect.y,'savedframe.png')  # spawn marker

                # file_to_open = image_folder / 'savedframe.png'
                # marker = Marker(50, 50, 375000, str(file_to_open))
                marker = Marker(player.rect.x,player.rect.y,'savedframe.png')  # spawn marker

                # os.chdir(r'C:\Users\Georg\Documents\Python Scripts\delta_bot\calibration')
                all_sprites_list.add(marker)

            # delete last saved position
            elif event.key == pygame.K_BACKSPACE:
                print(experiment_positions)
                experiment_positions.pop()
                marker.kill()
                marker.remove()
                position_number -= 1
                print(experiment_positions)
                # all_sprites_list.delete(-1)

            elif event.key == pygame.K_x:
                print(f"Deleting all {experiment_positions} positions")
                # positions are removed
                del experiment_positions[:]
                # counter setback
                position_number = 0

                #this removes all sprites, also the player..
                for marker in all_sprites_list:
                    marker.kill()
                    print("pos deleted")
                #therefore, add player again
                all_sprites_list.add(player)

            #take picture on button p release
            elif event.key == pygame.K_p:
                print("Actual position at: ")
                print(player.rect.x*multipl)
                print(player.rect.y*multipl)
                print(player.z)
                print(f"""x,y,z positions are: x={player.rect.x*multipl}
                    , y={player.rect.y*multipl}, z={player.z}""")


            # send position to microscope on button s release
            elif event.key == pygame.K_s:
                print("Player position at: ")
                print(player.rect.x)
                print(player.rect.y)
                print(player.z)
                print(f"""x,y,z positions are: x={player.rect.x*multipl}, y={player.rect.y*multipl}, z={player.z}""")
                test_position = Position("test_pos", player.rect.x*multipl, player.rect.x*multipl, player.z, comport="COM3")
                test_position.send_motor_values()

            #do something on button q release: qued picture taking
            elif event.key == pygame.K_q:
                print("Automated movement starting...")
                pictures_at_positions(experiment_positions)
            #do something on button c release: calibration
            elif event.key == pygame.K_c:
                iterations = 10
                print(f"Automated calibration starting with {iterations} iterations.")
                analyze_and_calibrate(iterations)
                #calibration_pictures(100000, 1)
            #do something on button f release: autofocus
            elif event.key == pygame.K_f:
                print("Automated focusing starting...")
                new_z_focus = autofocus(player.rect.x*multipl, player.rect.y*multipl, player.z, 10, 1000) #starts autofocus with 1 iterations
                player.z = new_z_focus
                print(f"New z focus position at: {player.z}")

    # This actually moves the player block based on the current speed
    player.update()

    # -- Draw everything
    # Clear screen
    #screen.fill(WHITE)
    screen.blit(backdrop, backdropbox)

    # Draw sprites
    all_sprites_list.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(60)

pygame.quit()
