from global_vars import *
import pygame
import math
import random
from pygame.locals import *


class PowerUp:
    spriteLaser = pygame.image.load('Sprites/PowerUps/laserDrop.png')
    #spriteBounce = pygame.image.load('Sprites/PowerUps/bounceDrop.png')
    #spriteSin = pygame.image.load('Sprites/PowerUps/sinDrop.png')
    def __init__(self, x, y):
        self.tag = "powerup"
        self.width = 16
        self.height = 16
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.index = 0 # random.randint(0, 2)
        self.type = "null"
        self.dead = False
        if (self.index == 0):
            self.type = "laser"
            self.surface = pygame.transform.scale(PowerUp.spriteLaser, (self.width, self.height))
        elif (self.index == 1):
            self.type = "bounce_bullet"
        elif (self.index == 2):
            self.type = "sin_bullet"


    def draw(self):
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        DISPLAYSURF.blit(self.surface, self.rect)

    def update(self):
        self.y += 3
        if (self.y > WINDOW_H):
            self.dead = True

    def OnCollide(self, ship):
        self.dead = True
        
    
