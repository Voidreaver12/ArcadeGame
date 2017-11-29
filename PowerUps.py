from global_vars import *
import pygame
import math
import random
from pygame.locals import *


class PowerUp:
    spriteLaser = pygame.image.load('Sprites/PowerUps/laserDrop1.png')
    spriteBounce = pygame.image.load('Sprites/PowerUps/bulletBounceDrop.png')
    spriteSin = pygame.image.load('Sprites/PowerUps/bulletSinDrop.png')
    spriteSplit = pygame.image.load('Sprites/PowerUps/bulletSplitDrop.png')

    def __init__(self, x, y):
        self.tag = "powerup"
        self.width = 32
        self.height = 32
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.index = random.randint(0, 3)
        self.type = "null"
        self.dead = False
        if (self.index == 0):
            self.type = "laser"
            self.surface = pygame.transform.scale(PowerUp.spriteLaser, (self.width, self.height))
        elif (self.index == 1):
            self.type = "bounce_bullet"
            self.surface = pygame.transform.scale(PowerUp.spriteBounce, (self.width, self.height))
        elif (self.index == 2):
            self.type = "sin_bullet"
            self.surface = pygame.transform.scale(PowerUp.spriteSin, (self.width, self.height))
        elif (self.index == 3):
            self.type = "split_bullet"
            self.surface = pygame.transform.scale(PowerUp.spriteSplit, (self.width, self.height))


    def draw(self):
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        DISPLAYSURF.blit(self.surface, self.rect)

    def update(self):
        self.y += 3
        if (self.y > WINDOW_H):
            self.dead = True

    def OnCollide(self, ship):
        self.dead = True
        
    
