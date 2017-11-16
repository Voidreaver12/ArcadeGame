import global_vars
from global_vars import *
import time
import random
import pygame
import math
if (ONPI): import RPi.GPIO as GPIO
from pygame.locals import *

# Laser class
class Laser:
    width = 9
    height = int(WINDOW_H/2)
    sprite0 = pygame.image.load('Sprites/Laser/laser0.png')
    sprite1 = pygame.image.load('Sprites/Laser/laser1.png')
    sprite2 = pygame.image.load('Sprites/Laser/laser2.png')
    spritePowerUp = pygame.image.load('Sprites/Laser/laserPowerUp.png')
    
    def __init__(self, x, y):
        self.x = x - Laser.width/2
        self.y = y - Laser.height
        self.damage = 1
        self.timeToLive = 100
        self.sprite = Laser.sprite0
        self.spriteIndex = 0
        self.dead = False
        
    def draw(self):
        self.rect = pygame.Rect( (self.x, self.y, Laser.width, Laser.height) )
        self.surface = pygame.transform.scale(self.sprite, (Laser.width, Laser.height))
        DISPLAYSURF.blit(self.surface, self.rect)

    def update(self, shipx, shipy):
        self.timeToLive -= 1
        if (self.timeToLive < 0):
            self.dead = True
        self.x = shipx - Laser.width/2
        self.y = shipy - Laser.height
        self.spriteIndex += 0.5
        if (self.spriteIndex >= 1.0):
            self.sprite = Laser.sprite1
        if (self.spriteIndex >= 2.0):
            self.sprite = Laser.sprite2
        if (self.spriteIndex >= 3.0):
            self.spriteI = Laser.sprite0
            self.spriteIndex = 0.0
        
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
        print(enemy)
        try:
            enemy.reduceHealth(self.damage)
        except:
            no = False
            #print("no damage funciton to call")
        self.dead = True

    def draw(self):
        self.rect = pygame.Rect( (self.x, self.y, Bullet.width, Bullet.height) )
        DISPLAYSURF.blit(Bullet.surface, self.rect)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if (self.y < 0):
            self.dead = True

class BounceBullet(Bullet):
    def __init__(self, x, y, vx, vy):
        Bullet.__init__(self,x, y, vx, vy)
    def update(self):
        Bullet.update(self)
        if (self.x < 0 or self.x > WINDOW_W):
            self.vx = self.vx*-1

class SplitBullet(Bullet):
    splitHeight = 200
    def __init__(self, x, y, vx, vy, ship):
        Bullet.__init__(self,x, y, vx, vy)
        self.ship = ship
    def update(self):
        Bullet.update(self)
        if (self.y < self.splitHeight):
            bullet = Bullet(self.x, self.y, 5, -3)
            self.ship.bullets.append(bullet)
            bullet = Bullet(self.x, self.y, -5, -3)
            self.ship.bullets.append(bullet)
            bullet = Bullet(self.x, self.y, 2, -5)
            self.ship.bullets.append(bullet)
            bullet = Bullet(self.x, self.y, -2, -5)
            self.ship.bullets.append(bullet)
            self.dead = True

class SinusoidalBullet(Bullet):
    def __init__(self, x, y, vx, vy, amplitude = 5, freq = 1, t = 0):
        Bullet.__init__(self,x, y, vx, vy)
        self.amplitiude = amplitude
        self.freq = freq
        self.t = t
    def update(self):
        Bullet.update(self)
        self.t += 1
        self.x += self.amplitiude*math.sin(self.t*self.freq)
                   
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
        self.weaponType = "basic"
        self.hasLaser = True
        self.lasers = []

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
            self.shoot()

    def shoot(self):
        if (self.weaponType == "basic"):
            bullet = Bullet(self.x + self.width/2, self.y, 0, -9)
            self.bullets.append(bullet)
        if (self.weaponType == "bounce"):
            bullet = BounceBullet(self.x + self.width/2, self.y, 7, -5)
            self.bullets.append(bullet)
            bullet = BounceBullet(self.x + self.width/2, self.y, 0, -7)
            self.bullets.append(bullet)
            bullet = BounceBullet(self.x + self.width/2, self.y, -7, -5)
            self.bullets.append(bullet)
        if (self.weaponType == "split"):
            bullet = SplitBullet(self.x + self.width/2, self.y, 0, -5, self)
            self.bullets.append(bullet)
        if (self.weaponType == "sin"):
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -5,5,0.5,0)
            self.bullets.append(bullet)
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -5,5,0.5,6)
            self.bullets.append(bullet)
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -5,15,0.2,15)
            self.bullets.append(bullet)
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -5,15,0.2,0)
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
        for l in self.lasers:
            if (l.dead):
                self.lasers.remove(l)
            else:
                l.update(self.x + self.width/2, self.y)
        
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
            elif (GPIO.input(LEFT) == True or key[pygame.K_a]): # left
                self.x -= self.MOVE_SPEED
                if (self.x + self.width/2 < 0):
                    self.x = WINDOW_W - self.width/2
            if(key[pygame.K_SPACE] and self.ready == True):
               self.shoot()
               self.ready = False
            elif (not(key[pygame.K_SPACE]) and self.ready == False):
                self.ready = True
            if (GPIO.input(ALT_SHOOT) == False and self.hasLaser == True):
                self.hasLaser = False
                laser = Laser(self.x + self.width/2, self.y)
                self.lasers.append(laser)                
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
            if (key[pygame.K_l] and self.hasLaser == True):
                self.hasLaser = False
                laser = Laser(self.x + self.width/2, self.y)
                self.lasers.append(laser)
                
                    
    def draw(self):
        self.surface = pygame.transform.scale(self.currentSprite, (self.width, self.height))
        self.rect = pygame.Rect( (self.x, self.y, self.width, self.height) )
        DISPLAYSURF.blit(self.surface, self.rect)
        for b in self.bullets:
            b.draw()
        if (self.hasLaser):
            laserposx = 10
            laserposy = 10 + (self.width/2 + 5)
            lasersurface = pygame.transform.scale(Laser.spritePowerUp, (99, 9))
            laserrect = pygame.Rect((laserposx, laserposy, 99, 9))
            DISPLAYSURF.blit(lasersurface, laserrect)
        for l in self.lasers:
            l.draw()
        for i in range(self.health):
            healthposx = (i*(self.width/2 + 5)) + 10
            healthposy = 10
            healthsurface = pygame.transform.scale(self.img1, (int(self.width/2), int(self.height/2)))
            healthrect = pygame.Rect( (healthposx, healthposy, self.width/2, self.height/2) )
            DISPLAYSURF.blit(healthsurface, healthrect)
            

    def OnCollide(self, enemy):
        self.health -= 1
        enemy.destroy()
        if (self.health <= 0):
            self.dead = True
