import pygame
from global_vars import *
import random



class Asteroid:
    padding = 20
    def __init__(self):
        border = random.randint(0, 1)
        self.x = 0
        self.y = 0
        self.width = 16
        self.height = 16
        self.vx = 0
        self.vy = 0
        if (border == 0): # on sides
            whichside = random.randint(0, 1)
            if (whichside == 0): # left
                self.x = -self.width
            elif (whichside == 1): # right
                self.x = WINDOW_W
            self.y = random.randint(-self.height, WINDOW_H)
        elif (border == 1): # on top/bottom
            whichside = random.randint(0, 1)
            if (whichside == 0): # top
                self.y = -self.height
            elif (whichside == 1): # bottom
                self.y = WINDOW_H
            self.x = random.randint(-self.width, WINDOW_W)
            
                
