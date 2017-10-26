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

# Setup Stuff
FPS = 30
WINDOW_W = 640
WINDOW_H = 480


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# Main loop
while True:
    if (GPIO.input(18) == False):
        print("UP")
    if (GPIO.input(19) == False):
        print("LEFT")
    if (GPIO.input(20) == False):
        print("DOWN")
    if (GPIO.input(21) == False):
        print("RIGHT")
        
