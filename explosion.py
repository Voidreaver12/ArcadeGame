from global_vars import *
import pygame

class Explosion:
    sprite0 = pygame.image.load('Sprites/Explosion/explosion0.png')
    sprite1 = pygame.image.load('Sprites/Explosion/explosion1.png')
    sprite2 = pygame.image.load('Sprites/Explosion/explosion2.png')
    sprite3 = pygame.image.load('Sprites/Explosion/explosion3.png')
    sprite4 = pygame.image.load('Sprites/Explosion/explosion4.png')
    sprite5 = pygame.image.load('Sprites/Explosion/explosion5.png')
    sprite6 = pygame.image.load('Sprites/Explosion/explosion6.png')
    sprite7 = pygame.image.load('Sprites/Explosion/explosion7.png')

    def __init__(self, x, y):
        self.width = 32
        self.height = 32
        self.x = x - self.width/2
        self.y = y - self.height/2
        self.spriteIndex = 0
        self.surface = pygame.transform.scale(Explosion.sprite0, (self.width, self.height))
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        self.dead = False

    def update(self):
        spriteIndex += 1
        if (spriteIndex == 2):
            self.surface = pygame.transform.scale(Explosion.sprite1, (self.width, self.height))
        elif (spriteIndex == 4):
            self.surface = pygame.transform.scale(Explosion.sprite2, (self.width, self.height))
        elif (spriteIndex == 6):
            self.surface = pygame.transform.scale(Explosion.sprite3, (self.width, self.height))
        elif (spriteIndex == 8):
            self.surface = pygame.transform.scale(Explosion.sprite4, (self.width, self.height))
        elif (spriteIndex == 10):
            self.surface = pygame.transform.scale(Explosion.sprite5, (self.width, self.height))
        elif (spriteIndex == 12):
            self.surface = pygame.transform.scale(Explosion.sprite6, (self.width, self.height))
        elif (spriteIndex == 14):
            self.surface = pygame.transform.scale(Explosion.sprite7, (self.width, self.height))
        elif (spriteIndex >= 16):
            self.dead = False

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.rect)
