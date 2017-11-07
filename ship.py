import global_vars
from global_vars import *
import time
import random
import pygame
import math
if (ONPI): import RPi.GPIO as GPIO
from pygame.locals import *

# Bullet class
class Bullet:
    width = 6
    height = 8
    sprite = pygame.image.load('Sprites/sprite_shot.png')
    surface = pygame.transform.scale(sprite, (width, height))
    def __init__(self, x, y, vx, vy):
        self.x = x - Bullet.width/2
        self.y = y 
        self.damage = 1
        self.vx = vx
        self.vy = vy
        self.dead = False
        
    def OnCollide(self, enemy):
        enemy.reduceHealth(self.damage)
        self.dead = True

    def draw(self):
        self.rect = pygame.Rect( (self.x, self.y, Bullet.width, Bullet.height) )
        DISPLAYSURF.blit(Bullet.surface, self.rect)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if (self.y < 0):
            self.dead = True

# Ship class
class Ship:
    def __init__(self, x=WINDOW_W/2, y=WINDOW_H*3/4, h=5):
        self.health = h
        self.MOVE_SPEED = 3
        self.loadSprites()
        self.width = 34
        self.height = 32
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.bullets = []
        self.dead = False
        self.ready = False

    def loadSprites(self):
        self.img0 = pygame.image.load('Sprites/PlayerShip/sprite_ship0.png')
        self.img1 = pygame.image.load('Sprites/PlayerShip/sprite_ship1.png')
        self.img2 = pygame.image.load('Sprites/PlayerShip/sprite_ship2.png')
        self.img3 = pygame.image.load('Sprites/PlayerShip/sprite_ship3.png')
        self.img4 = pygame.image.load('Sprites/PlayerShip/sprite_ship4.png')
        self.currentSprite = self.img0
        self.spriteIndex = 0

    def __call__(self, channel):
        time.sleep(0.005)
        if (GPIO.input(channel)):
            slef.shoot()

    def shoot(self):
        bullet = Bullet(self.x + self.width/2, self.y, 0, -5)
        self.bullets.append(bullet)

    def update(self):
        self.move()
        self.updateSprite()
        for b in self.bullets:
            if (b.dead):
                self.bullets.remove(b)
                #print("removed bullet")
                #print(len(self.bullets))
            else:
                b.update()
        
    def updateSprite(self):
        self.spriteIndex += 1
        if (self.spriteIndex >= 50):
            self.spriteIndex = 0
        if (self.spriteIndex == 0):
            self.currentSprite = self.img0
        elif (self.spriteIndex == 10):
            self.currentSprite = self.img1
        elif (self.spriteIndex == 20):
            self.currentSprite = self.img2
        elif (self.spriteIndex == 30):
            self.currentSprite = self.img3
        elif (self.spriteIndex == 40):
            self.currentSprite = self.img4

    def move(self):
        key = pygame.key.get_pressed()
        if (ONPI):
            if (GPIO.input(UP) == False or key[pygame.K_w]): # up
                self.y -= self.MOVE_SPEED
                if (self.y < WINDOW_H/2):
                    self.y = WINDOW_H/2
            elif (GPIO.input(DOWN) == False or key[pygame.K_s]): # down
                self.y += self.MOVE_SPEED
                if (self.y + self.height > WINDOW_H):
                    self.y = WINDOW_H - self.height
            if (GPIO.input(RIGHT) == False or key[pygame.K_d]): # right
                self.x += self.MOVE_SPEED
                if (self.x + self.width/2 > WINDOW_W):
                    self.x = 0 - self.width/2
            elif (GPIO.input(LEFT) == False or key[pygame.K_a]): # left
                self.x -= self.MOVE_SPEED
                if (self.x + self.width/2 < 0):
                    self.x = WINDOW_W - self.width/2
            if(key[pygame.K_SPACE] and self.ready == True):
               self.shoot()
               self.ready = False
            elif (not(key[pygame.K_SPACE]) and self.ready == False):
                self.ready = True
        #if testing without the RPi
        else:
            if (key[pygame.K_w]): # up
                self.y -= self.MOVE_SPEED
                if (self.y < WINDOW_H/2):
                    self.y = WINDOW_H/2
            elif (key[pygame.K_s]): # down
                self.y += self.MOVE_SPEED
                if (self.y + self.height > WINDOW_H):
                    self.y = WINDOW_H - self.height
            if (key[pygame.K_d]): # right
                self.x += self.MOVE_SPEED
                if (self.x + self.width/2 > WINDOW_W):
                    self.x = 0 - self.width/2
            elif (key[pygame.K_a]): # left
                self.x -= self.MOVE_SPEED
                if (self.x + self.width/2 < 0):
                    self.x = WINDOW_W - self.width/2
            if(key[pygame.K_SPACE] and self.ready == True):
               self.shoot()
               self.ready = False
            elif (not(key[pygame.K_SPACE]) and self.ready == False):
                self.ready = True
                    
    def draw(self):
        self.surface = pygame.transform.scale(self.currentSprite, (self.width, self.height))
        self.rect = pygame.Rect( (self.x, self.y, self.width, self.height) )
        DISPLAYSURF.blit(self.surface, self.rect)
        for b in self.bullets:
            b.draw()

    def OnCollide(self, enemy):
        self.health -= 1
        enemy.destroy()
        if (self.health <= 0):
            self.dead = True
