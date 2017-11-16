import random
import pygame
import time
import math
import json

XOFF = 50
YOFF = 50
DX = 40
DY = 40

class BasicMovement:
    def __init__(self,path,speed,manager,xpos,ypos):
        self.path = path
        self.speed = speed
        self.ReadFile(path)
        self.manager = manager
        self.xpos = xpos
        self.ypos = ypos

    def ReadFile(self,path):
        f = open(path,'r')
        self.pathCords = [[int(x) for x in line.split()] for line in f]
        #self.x = self.pathCords[0][0]
        #self.y = self.pathCords[0][1]
        self.step = 1

    def UpdatePosition(self):
        if (self.step < len(self.pathCords)):
            dx = self.pathCords[self.step][0] - self.x
            dy = self.pathCords[self.step][1] - self.y
            totalDistance = math.sqrt(math.pow(dx,2)+math.pow(dy,2))
            if (totalDistance < self.speed):
                self.step += 1
            else:
                self.x += (dx/totalDistance)*self.speed
                self.y += (dy/totalDistance)*self.speed
        else:
            xgoal = self.xpos*DX + XOFF + self.manager.wiggle
            ygoal = self.ypos*DY + YOFF
            dx = xgoal - self.x
            dy = ygoal - self.y
            totalDistance = math.sqrt(math.pow(dx,2)+math.pow(dy,2))
            if (totalDistance < self.speed):
                self.x = xgoal
                self.y = ygoal
            else:
                self.x += (dx/totalDistance)*self.speed
                self.y += (dy/totalDistance)*self.speed

class Test(BasicMovement):
    def __init__(self,path,speed):
        BasicMovement.__init__(self,path,speed)

    def PrintPosition(self):
        print(self.x,self.y)
        

#test = Test("Paths/test.txt",1)
#test.PrintPosition()
#while(1):
#    test.UpdatePosition()
#    test.PrintPosition()
#    time.sleep(0.01)

        
