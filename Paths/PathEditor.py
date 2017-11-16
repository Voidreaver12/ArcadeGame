import random
import pygame
import time
import math
import json
from global_vars import *
from pygame.locals import *
fileName = "Paths\text.txt"

points = []

pygame.init()
pygame.display.set_caption('Path Creator')
f = open(fileName,'w+')
while(True):
    for event in pygame.event.get():
        if event.type == QUIT:
            f.close()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            points.append(pygame.mouse.get_pos())
            x, y = pygame.mouse.get_pos()
            f.write(str(x) + " " + str(y)+"\n")
            
    
    
    DISPLAYSURF.fill((0, 0, 0))
    if (len(points) > 1):
        pygame.draw.lines(DISPLAYSURF, 0xfffff , False, points, 3) #dont know why this doesnt work
    pygame.display.update()
