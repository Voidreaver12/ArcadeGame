# Authors: Noah Deibert, Mark Reifsteck
# 
#
#

# Imports
import time
import RPi.GPIO as GPIO
import numpy as np
import random
import sys
import math
import pygame
from pygame.locals import *

# Global Variables
FPS = 30
WINDOW_W = 640
WINDOW_H = 480

# Ship class
class Ship:
    def __init__(self, x=WINDOW_W/2, y=WINDOW_H/4, h=10):
        self.x = x
        self.y = y
        self.health = h
        self.MOVE_SPEED = 1

    def __call__(self, channel):
        time.sleep(0.005)
        if (GPIO.input(channel)):
            print("bang")

    def move(self):
        if (GPIO.input(18) == False):
            self.y += self.MOVE_SPEED
        else if (GPIO.input(20) == False):
            self.y -= self.MOVE_SPEED
        if (GPIO.input(19) == False):
            self.x += self.MOVE_SPEED
        else if (GPIO.input(21) == False):
            self.x -= self.MOVE_SPEED


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Movement
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # UP
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # RIGHT
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP) # DOWN
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) # LEFT
# Shooting
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Shoot
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Special Shoot





# Main
try:
    # Setup window
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption('Arcade Game')
    # Setup ship
    ship = Ship()
    # Event detection for shooting
    GPIO.add_event_detect(22, GPIO.RISING, callback = ship, bouncetime = 25)
    # Main loop
    while True:
        # Process pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # move ship every frame
        ship.move()
        # sleep
        time.sleep(0.1)


# Process CTRL C
except(KeyboardInterrupt, SystemExit):
    print("\nCTRL-C detected, exiting.")
    GPIO.cleanup()
