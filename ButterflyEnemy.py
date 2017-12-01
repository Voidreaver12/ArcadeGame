import global_vars
from global_vars import *
import time
import random
import pygame
import math
from EnemyMovement import *

class ButterflyEnemy(BasicMovement):
    def __init__(self,x,y,path,speed,manager,xpos,ypos,health):
        BasicMovement.__init__(self,path,speed,manager,xpos,ypos)
        self.x = x
        self.y = y
        self.width = 39
        self.height = 39
        self.health = health
        self.dead = False
        self.loadSprites()
        #self.manager = manager

    def loadSprites(self):
        self.img0 = pygame.image.load('Sprites/EnemyButterfly/sprite_enemybutterfly0.png')
        self.img1 = pygame.image.load('Sprites/EnemyButterfly/sprite_enemybutterfly1.png')
        self.currentSprite = self.img0
        #self.spriteIndex = self.manager.spriteIndexButterfly
        
    def reduceHealth(self, damage):
        health -= damage
        if (health <= 0):
            self.dead = True
            print("im dead")

    def OnCollide(self, hit):
        self.health -= hit.damage
        if (self.health <= 0):
            self.dead = True

    def NewPath(self, path):
        BasicMovement.ReadFile(self, path)

    def update(self):
        BasicMovement.UpdatePosition(self)
        if (self.manager.spriteIndexButterfly == 0):
            self.currentSprite = self.img0
        elif (self.manager.spriteIndexButterfly == 20):
            self.currentSprite = self.img1

    def draw(self):
        self.surface = pygame.transform.scale(self.currentSprite, (self.width, self.height))
        self.rect = pygame.Rect( (self.x, self.y, self.width, self.height) )
        DISPLAYSURF.blit(self.surface, self.rect)

    def destroy(self):
        print("autodestruction")
        self.dead = True

    



    
        
