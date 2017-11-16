import global_vars
from global_vars import *
import time
import random
import pygame
import math
import ButterflyEnemy
import FlyEnemy

FREQ = 45

class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.wiggle = -30
        self.up = True
        self.spriteIndexButterfly = 0
        self.ReadFile("Levels/level1.txt")
        
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
        self.time += 1

        if (self.index < len(self.enemyFile) and self.time >= int(self.enemyFile[self.index][0])):
            if (self.enemyFile[self.index][1] == 'b'):
                x = int(self.enemyFile[self.index][2])
                y = int(self.enemyFile[self.index][3])
                path = self.enemyFile[self.index][6]
                speed = int(self.enemyFile[self.index][7])
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
                xpos = int(self.enemyFile[self.index][4])
                ypos = int(self.enemyFile[self.index][5])
                fly = FlyEnemy.FlyEnemy(x,y,path,speed,self,xpos,ypos,1)
                self.enemies.append(fly)
                self.index += 1
            elif (self.enemyFile[self.index][1] == 'DONE'):
                self.done = True

        if (self.done == True and self.time%FREQ == 0 and len(self.enemies) != 0):
            r = random.randint(0,len(self.enemies)-1)
            if (self.enemies[r].step >= len(self.enemies[r].pathCords)):
                r2 = random.randint(0,2)
                if (r2 == 0):
                    self.enemies[r].NewPath("Paths/attack.txt")
                elif (r2 == 1):
                    self.enemies[r].NewPath("Paths/attackl.txt")
                elif (r2 == 2):
                    self.enemies[r].NewPath("Paths/attackr.txt")
                print("attacking")
       
        self.spriteIndexButterfly += 1
        if (self.spriteIndexButterfly >= 40):
            self.spriteIndexButterfly = 0
            
            

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    
