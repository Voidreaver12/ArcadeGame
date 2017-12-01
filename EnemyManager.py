import global_vars
from global_vars import *
import time
import random
import pygame
import math
import ButterflyEnemy
import FlyEnemy
import MantisEnemy
import GameUtility

FREQ = 45
DIF_MOD = 3

class EnemyManager:
    def __init__(self, ship):
        self.enemies = []
        self.wiggle = -30
        self.up = True
        self.spriteIndexButterfly = 0
        self.ReadFile("Levels/level1.txt")
        self.level = 1
        self.ship = ship
        self.FREQ = FREQ
        
    def ReadFile(self, path):
        f = open(path, 'r')
        self.enemyFile = [[x for x in line.split()] for line in f]
        self.done = False
        self.index = 0
        self.time = 0
        # 0:time, 1:enemy type, 2:x, 3:y, 4:xpos, 5:ypos, 6:pathPath, 7:speed
        # enemy type: b = butterfly, f = fly
    
    def update(self):
        if (self.up == True):
            self.wiggle += 1
            if (self.wiggle == 30):
                self.up = False
        else:
            self.wiggle -= 1
            if (self.wiggle == -30):
                self.up = True
                
        for enemy in self.enemies:
            enemy.update()
            GameUtility.CheckCollide(enemy,self.ship)
            
        self.time += 1

        while (self.index < len(self.enemyFile) and self.time >= int(self.enemyFile[self.index][0])):
            if (self.enemyFile[self.index][1] == 'b'):
                x = int(self.enemyFile[self.index][2])
                y = int(self.enemyFile[self.index][3])
                path = self.enemyFile[self.index][6]
                speed = int(self.enemyFile[self.index][7])
                if (self.level > 5):
                    speed += (self.level-5)*DIF_MOD
                xpos = int(self.enemyFile[self.index][4])
                ypos = int(self.enemyFile[self.index][5])
                butterfly = ButterflyEnemy.ButterflyEnemy(x,y,path,speed,self,xpos,ypos,1)
                self.enemies.append(butterfly)
                self.index += 1
            elif (self.enemyFile[self.index][1] == 'f'):
                x = int(self.enemyFile[self.index][2])
                y = int(self.enemyFile[self.index][3])
                path = self.enemyFile[self.index][6]
                speed = int(self.enemyFile[self.index][7])
                if (self.level > 5):
                    speed += (self.level-5)*DIF_MOD
                xpos = int(self.enemyFile[self.index][4])
                ypos = int(self.enemyFile[self.index][5])
                fly = FlyEnemy.FlyEnemy(x,y,path,speed,self,xpos,ypos,1)
                self.enemies.append(fly)
                self.index += 1
            elif (self.enemyFile[self.index][1] == 'm'):
                x = int(self.enemyFile[self.index][2])
                y = int(self.enemyFile[self.index][3])
                path = self.enemyFile[self.index][6]
                speed = int(self.enemyFile[self.index][7])
                if (self.level > 5):
                    speed += (self.level-5)*DIF_MOD
                xpos = int(self.enemyFile[self.index][4])
                ypos = int(self.enemyFile[self.index][5])
                mantis = MantisEnemy.MantisEnemy(x,y,path,speed,self,xpos,ypos,3)
                self.enemies.append(mantis)
                self.index += 1
            elif (self.enemyFile[self.index][1] == 'DONE'):
                self.done = True
                self.index += 1

        if ((self.done == True or self.level > 4) and self.time%FREQ == 0 and len(self.enemies) != 0):
            r = random.randint(0,len(self.enemies)-1)
            if (self.enemies[r].step >= len(self.enemies[r].pathCords) or self.level > 5):
                r2 = random.randint(0,3)
                if (r2 == 0):
                    self.enemies[r].NewPath("Paths/attack.txt")
                elif (r2 == 1):
                    self.enemies[r].NewPath("Paths/attackl.txt")
                elif (r2 == 2):
                    self.enemies[r].NewPath("Paths/attackr.txt")
                elif (r2 == 3):
                    self.enemies[r].NewPath("Paths/attackM.txt")
                #print("attacking")
       
        self.spriteIndexButterfly += 1
        if (self.spriteIndexButterfly >= 40):
            self.spriteIndexButterfly = 0
            
        if (len(self.enemies) == 0):
            self.nextLevel()

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    def nextLevel(self):
        print("LEVEL COMPLETE")
        self.level += 1
        self.done = False
        if (self.level <= 5):
            self.ReadFile("Levels/level" + str(self.level) + ".txt")
        else:
            self.ReadFile("Levels/level" + str(5) + ".txt")
            self.FREQ -= 5
        

    
