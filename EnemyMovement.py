import random
import pygame
import time
import math
import json

class BasicMovement:
    def __init__(self,path,speed):
        self.path = path
        self.speed = speed
        self.ReadFile(path)

    def ReadFile(self,path):
        f = open(path,'r')
        self.pathCords = [[int(x) for x in line.split()] for line in f]
        self.x = self.pathCords[0][0]
        self.y = self.pathCords[0][1]
        self.step = 1

    def UpdatePosition(self):
        dx = self.pathCords[self.step][0] - self.x
        dy = self.pathCords[self.step][1] - self.y
        totalDistance = math.sqrt(math.pow(dx,2)+math.pow(dy,2))
        if (totalDistance < self.speed):
            self.step += 1
        else:
            self.x += (dx/totalDistance)*self.speed
            self.y += (dy/totalDistance)*self.speed


class Test(BasicMovement):
    def __init__(self,path,speed):
        BasicMovement.__init__(self,path,speed)

    def PrintPosition(self):
        print(self.x,self.y)
        

test = Test("Paths/test.txt",1)
test.PrintPosition()
while(1):
    test.UpdatePosition()
    test.PrintPosition()
    time.sleep(0.01)

        
