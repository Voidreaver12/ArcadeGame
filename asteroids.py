import pygame
from global_vars import *
import random



class Asteroid:
    sprite0 = pygame.image.load('Sprites/Asteroids/asteroid0.png')
    sprite1 = pygame.image.load('Sprites/Asteroids/asteroid1.png')
    sprite2 = pygame.image.load('Sprites/Asteroids/asteroid2.png')
    sprite3 = pygame.image.load('Sprites/Asteroids/asteroid3.png')
    sprite4 = pygame.image.load('Sprites/Asteroids/asteroid4.png')
    sprite5 = pygame.image.load('Sprites/Asteroids/asteroid5.png')
    sprite6 = pygame.image.load('Sprites/Asteroids/asteroid6.png')
    sprite7 = pygame.image.load('Sprites/Asteroids/asteroid7.png')
    def __init__(self):
        border = random.randint(0, 1)
        self.x = 0
        self.y = 0
        self.width = random.randint(16, 48) #32
        self.height = self.width #32
        self.padding = 20
        self.vx = 0
        self.vy = 0
        self.currentSprite = Asteroid.sprite0
        self.spriteIndex = 0.0
        if (border == 0): # on sides
            whichside = random.randint(0, 1)
            if (whichside == 0): # left
                self.x = -self.width
                self.vx = 1
            elif (whichside == 1): # right
                self.x = WINDOW_W
                self.vx = -1
            self.vx *= random.random() * 5.0
            self.vy = random.random() * 10.0 - 5.0
            self.y = random.randint(-self.height, WINDOW_H)
        elif (border == 1): # on top/bottom
            whichside = random.randint(0, 1)
            if (whichside == 0): # top
                self.y = -self.height
                self.vy = 1
            elif (whichside == 1): # bottom
                self.y = WINDOW_H
                self.vy = -1
            self.vy *= random.random() * 5.0
            self.vx = random.random() * 10 - 5.0
            self.x = random.randint(-self.width, WINDOW_W)
            
    def checkBounds(self):
        if (self.vx >= 0.0 and self.x >= WINDOW_W-self.width):
            self.vx *= -1
        if (self.vx <= 0.0 and self.x <= 0.0):
            self.vx *= -1
        if (self.vy >= 0.0 and self.y >= WINDOW_H-self.height):
            self.vy *= -1
        if (self.vy <= 0.0 and self.y <= 0.0):
            self.vy *= -1
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.checkBounds()
        self.spriteIndex += 0.25
        if   (self.spriteIndex >= 8.0):
            self.spriteIndex = 0.0
            self.currentSprite = Asteroid.sprite0
        elif (self.spriteIndex >= 7.0):
            self.currentSprite = Asteroid.sprite7
        elif (self.spriteIndex >= 6.0):
            self.currentSprite = Asteroid.sprite6
        elif (self.spriteIndex >= 5.0):
            self.currentSprite = Asteroid.sprite5
        elif (self.spriteIndex >= 4.0):
            self.currentSprite = Asteroid.sprite4
        elif (self.spriteIndex >= 3.0):
            self.currentSprite = Asteroid.sprite3
        elif (self.spriteIndex >= 2.0):
            self.currentSprite = Asteroid.sprite2
        elif (self.spriteIndex >= 1.0):
            self.currentSprite = Asteroid.sprite1


    def draw(self):
        self.surface = pygame.transform.scale(self.currentSprite, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        DISPLAYSURF.blit(self.surface, self.rect)







