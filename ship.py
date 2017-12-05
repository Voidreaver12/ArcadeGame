import time
import random
import pygame
import math
from global_vars import *
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
        self.width = 9
        self.height = int(WINDOW_H/2)
        self.x = x - Laser.width/2
        self.y = y - Laser.height
        self.damage = 0.2
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
            
    def OnCollide(self, enemy):
        try:
            enemy.reduceHealth(self.damage)
        except:
            no = False
            #print("no damage function to call")
            
        
# Bullet class
class Bullet:
    width = 9
    height = 12
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
        #print(enemy)
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
    splitHeight = WINDOW_H*0.4
    def __init__(self, x, y, vx, vy, ship):
        Bullet.__init__(self,x, y, vx, vy)
        self.ship = ship
    def update(self):
        Bullet.update(self)
        if (self.y < self.splitHeight):
            bullet = Bullet(self.x, self.y, 5, -7)
            self.ship.bullets.append(bullet)
            bullet = Bullet(self.x, self.y, -5, -7)
            self.ship.bullets.append(bullet)
            bullet = Bullet(self.x, self.y, 2, -9)
            self.ship.bullets.append(bullet)
            bullet = Bullet(self.x, self.y, -2, -9)
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
        self.MOVE_SPEED = 10
        self.loadSprites()
        self.width = 51
        self.height = 48
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.bullets = []
        self.dead = False
        self.ready = False
        self.weaponType = "basic"
        self.hasLaser = True
        self.lasers = []
        self.damage = 10
        self.maxBulletTime = 100
        self.bulletTimer = 0
        self.game_state = 1

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
            print('game state: ' + str(self.game_state))
            if (self.game_state == 1):
                self.game_state = 2
            else:
                self.shoot()
            
    def call(self):
        if (HAS_GAME_BEGUN == 0):
            HAS_GAME_BEGUN = 1
        else:
            self.shoot()

    def shoot(self):
        if (self.weaponType == "basic"):
            bullet = Bullet(self.x + self.width/2, self.y, 0, -18)
            self.bullets.append(bullet)
        elif (self.weaponType == "bounce"):
            bullet = BounceBullet(self.x + self.width/2, self.y, 7, -9)
            self.bullets.append(bullet)
            bullet = BounceBullet(self.x + self.width/2, self.y, 0, -13)
            self.bullets.append(bullet)
            bullet = BounceBullet(self.x + self.width/2, self.y, -7, -9)
            self.bullets.append(bullet)
        elif (self.weaponType == "split"):
            bullet = SplitBullet(self.x + self.width/2, self.y, 0, -10, self)
            self.bullets.append(bullet)
        elif (self.weaponType == "sin"):
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -10,5,0.5,0)
            self.bullets.append(bullet)
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -10,5,0.5,6)
            self.bullets.append(bullet)
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -10,15,0.2,15)
            self.bullets.append(bullet)
            bullet = SinusoidalBullet(self.x + self.width/2, self.y, 0, -10,15,0.2,0)
            self.bullets.append(bullet)

    def update(self):
        if (self.health <= 0):
            self.game_state = 3
        self.move()
        self.updateSprite()
        self.bulletTimer -= 1
        if (self.bulletTimer <= 0):
            self.weaponType = "basic"
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
            

    def OnCollide(self, other):
        if (other.tag == "enemy"):
            self.health -= 1
            enemy.destroy()
            if (self.health <= 0):
                self.dead = True
        elif (other.tag == "powerup"):
            if (other.type == "laser"):
                self.hasLaser = True
            elif (other.type == "split_bullet"):
                self.bulletTimer = self.maxBulletTime
                self.weaponType = "split"
            elif (other.type == "bounce_bullet"):
                self.bulletTimer = self.maxBulletTime
                self.weaponType = "bounce"
            elif (other.type == "sin_bullet"):
                self.bulletTimer = self.maxBulletTime
                self.weaponType = "sin"

