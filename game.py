# Authors: Noah Deibert, Mark Reifsteck
# 
#
#

ONPI = True # a variable that controls whether or not to uses GPIO funcions

# Imports
import time
if ONPI:
    import RPi.GPIO as GPIO
#import numpy as np
import Stars
import random
import sys
import math
import pygame
from pygame.locals import *

# Global Variables
FPS = 30
WINDOW_W = 640
WINDOW_H = 480

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
            if (GPIO.input(18) == False or key[pygame.K_w]): # up
                self.y -= self.MOVE_SPEED
                if (self.y < WINDOW_H/2):
                    self.y = WINDOW_H/2
            elif (GPIO.input(20) == False or key[pygame.K_s]): # down
                self.y += self.MOVE_SPEED
                if (self.y + self.height > WINDOW_H):
                    self.y = WINDOW_H - self.height
            if (GPIO.input(19) == False or key[pygame.K_d]): # right
                self.x += self.MOVE_SPEED
                if (self.x + self.width/2 > WINDOW_W):
                    self.x = 0 - self.width/2
            elif (GPIO.input(21) == False or key[pygame.K_a]): # left
                self.x -= self.MOVE_SPEED
                if (self.x + self.width/2 < 0):
                    self.x = WINDOW_W - self.width/2
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

if (ONPI):
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
    # Setup stars
    stars = Stars.Stars(0,0,WINDOW_W, WINDOW_H,DISPLAYSURF)
    # Setup ship
    ship = Ship()
    # Event detection for shooting
    if (ONPI):
        GPIO.add_event_detect(22, GPIO.RISING, callback = ship, bouncetime = 25)
    # Main loop
    while True:
        # Process pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # move ship every frame
        ship.update()
        stars.updateStars()
        DISPLAYSURF.fill((0, 0, 0))
        ship.draw()
        stars.drawStars()
        pygame.display.update()
        # sleep
        #time.sleep(0.05)


# Process CTRL C
except(KeyboardInterrupt, SystemExit):
    print("\nCTRL-C detected, exiting.")
    if (ONPI):
        GPIO.cleanup()
