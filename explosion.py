from global_vars import *
import pygame

class Explosion:
    sprite0 = pygame.image.load('Sprites/Explosion/sprite_explosion0.png')
    sprite1 = pygame.image.load('Sprites/Explosion/sprite_explosion1.png')
    sprite2 = pygame.image.load('Sprites/Explosion/sprite_explosion2.png')
    sprite3 = pygame.image.load('Sprites/Explosion/sprite_explosion3.png')
    sprite4 = pygame.image.load('Sprites/Explosion/sprite_explosion4.png')
    
    def __init__(self, x, y):
        self.width = 48
        self.height = 48
        self.x = x - self.width
        self.y = y - self.height
        self.spriteIndex = 0.0
        self.surface = pygame.transform.scale(Explosion.sprite0, (self.width, self.height))
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        self.dead = False

    def update(self):
        self.spriteIndex += 0.2
        if (self.spriteIndex >= 5.0):
            self.dead = True
        elif (self.spriteIndex >= 4.0):
            self.surface = pygame.transform.scale(Explosion.sprite4, (self.width, self.height))
        elif (self.spriteIndex >= 3.0):
            self.surface = pygame.transform.scale(Explosion.sprite3, (self.width, self.height))
        elif (self.spriteIndex >= 2.0):
            self.surface = pygame.transform.scale(Explosion.sprite2, (self.width, self.height))
        elif (self.spriteIndex >= 1.0):
            self.surface = pygame.transform.scale(Explosion.sprite1, (self.width, self.height))

    def draw(self):
        DISPLAYSURF.blit(self.surface, self.rect)
