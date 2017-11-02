#import numpy as np
import random
import pygame
import time
import Stars

pygame.init()
DISPLAYSURF = pygame.display.set_mode((500, 500))
stars = Stars.Stars(0,0,500,500,DISPLAYSURF)
while(True):
    DISPLAYSURF.fill((0, 0, 0))
    stars.updateStars()
    stars.drawStars()
    pygame.display.update()
