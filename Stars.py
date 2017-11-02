#import numpy as np
import random
import pygame
import time

class Star:
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.speed = speed
    
class Stars:
    def __init__(self,xmin,ymin,xmax,ymax,DISPLAYSURF,speed = 1):
        self.DISPLAYSURF = DISPLAYSURF
        self.number = 100
        self.number2 = 20
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.speed = speed
        self.width = 64
        self.height = 64
        self.loadSprites()
        self.initializeStars()

    def loadSprites(self):
        self.img0 = pygame.image.load('Sprites/sprite_star.png')
        self.img1 = pygame.image.load('Sprites/sprite_bigstar.png')

    def initializeStars(self):
        self.starArray = []
        for x in range(self.number):
            self.starArray.append(Star(random.randint(self.xmin,self.xmax),random.randint(self.ymin,self.ymax),random.uniform(0.5,1.5)))
            
        self.starArray2 = []
        for x in range(self.number2):
            self.starArray2.append(Star(random.randint(self.xmin,self.xmax),random.randint(self.ymin,self.ymax),random.uniform(1.5,2.5)))

    def drawStars(self):
        for x in range(self.number):
            self.surface = pygame.transform.scale(self.img0, (self.width, self.height))
            self.rect = pygame.Rect( (self.starArray[x].x, self.starArray[x].y, self.width, self.height) )
            self.DISPLAYSURF.blit(self.surface, self.rect)
        for x in range(self.number2):
            self.surface = pygame.transform.scale(self.img1, (self.width, self.height))
            self.rect = pygame.Rect( (self.starArray2[x].x, self.starArray2[x].y, self.width, self.height) )
            self.DISPLAYSURF.blit(self.surface, self.rect)
        
    def updateStars(self):
        for x in range(self.number):
            self.starArray[x].y += self.starArray[x].speed
            if (self.starArray[x].y > self.ymax):
                self.starArray[x].y = 0 - random.randint(0,50)
                self.starArray[x].x = random.randint(self.xmin,self.xmax)
        for x in range(self.number2):
            self.starArray2[x].y += self.starArray2[x].speed
            if (self.starArray2[x].y > self.ymax):
                self.starArray2[x].y = 0 - random.randint(0,50)
                self.starArray2[x].x = random.randint(self.xmin,self.xmax)
            


