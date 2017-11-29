# Authors: Noah Deibert, Mark Reifsteck
# 
#
#

# Imports
import time
#import numpy as np
import Stars
import random
import sys
import math
import pygame
import SpecialBullets as b
from pygame.locals import *
from global_vars import *
import ship
import PowerUps
import asteroids
import explosion
import EnemyManager
import GameUtility
if (ONPI == True): import RPi.GPIO as GPIO

if (ONPI):
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Movement
    GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP) # UP
    GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # RIGHT
    GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # DOWN
    GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # LEFT
    # Shooting
    GPIO.setup(SHOOT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Shoot
    GPIO.setup(ALT_SHOOT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Special Shoot

# Main
try:
    # Setup window
    pygame.init()
    #DISPLAYSURF = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption('Arcade Game')
    # Setup stars
    stars = Stars.Stars(0,0,WINDOW_W, WINDOW_H,DISPLAYSURF)
    # Setup powerups, explosions
    powerups = []
    explosions = []
    rocks = []
    # Setup ship
    ship = ship.Ship()
    # Setup enemies
    enemies = EnemyManager.EnemyManager()
    # Event detection for shooting
    if (ONPI):
        GPIO.add_event_detect(SHOOT, GPIO.RISING, callback = ship, bouncetime = 25)
    # Main loop
    while True:
        start_time = time.time()
        # Process pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #################
        # Update things #
        #################
        ship.update()
        stars.updateStars()
        enemies.update()
        for p in powerups:
            p.update()
            if (p.dead):
                powerups.remove(p)
        for e in explosions:
            e.update()
            if (e.dead):
                explosions.remove(e)
        for r in rocks:
            r.update()
        if (random.randint(1,10) == 10):
            rock = asteroids.Asteroid()
            rocks.append(rock)
            print('added a rock')
        ########################
        # Check for collisions #
        ########################
        # Enemies
        for enemy in enemies.enemies:
            # Hit by bullets
            for bullet in ship.bullets:
                GameUtility.CheckCollide(enemy,bullet)
            # Hit by laser
            for laser in ship.lasers:
                GameUtility.CheckCollide(enemy, laser)
            # If they died, remove from array and drop powerup
            if (enemy.dead == True):
                enemies.enemies.remove(enemy)
                boom = explosion.Explosion(enemy.x+enemy.width, enemy.y+enemy.height)
                explosions.append(boom)
                if (random.randint(1, 10) == 10):
                    pup = PowerUps.PowerUp(enemy.x+enemy.width, enemy.y+enemy.height)
                    powerups.append(pup)
                    
        # Powerup collection by ship
        for p in powerups:
            GameUtility.CheckCollide(p, ship)

        ###############
        # Draw things #
        ###############
        DISPLAYSURF.fill((0, 0, 0))
        ship.draw()
        stars.drawStars()
        for p in powerups:
            p.draw()
        for e in explosions:
            e.draw()
        enemies.draw()
        for r in rocks:
            r.draw()
        pygame.display.update()
        
        # Sleep until next frame
        while(time.time() - start_time < 1/FPS):
            time.sleep(0.00000001)
        #print(time.time() - start_time)
        # sleep
        #time.sleep(0.05)


# Process CTRL C
except(KeyboardInterrupt, SystemExit):
    print("\nCTRL-C detected, exiting.")
    if (ONPI):
        GPIO.cleanup()
