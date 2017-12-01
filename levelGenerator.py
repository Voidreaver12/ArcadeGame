import random
import pygame
import time
import math
import json

f = open("LevelsTemp/newlevel.txt",'w+')
time = 0
enemies = []


while(True):
    selection = input("What do you want to add? enemies(1), change the time(2), or exit program(3)")
    if (selection == "1"):
        numberOfEnemies = int(input("How many? (24 per row)?"))
        offset = int(input("How much ofset for the columns?"))
        row = int(input("What row?"))
        typeOfEnemy = input("What type? (b)(f)(m)")
        path = "Paths/" + input("What path should they come in on?") + ".txt"
        speed = input("At what speed?")
        interval = int(input("A what interval?"))
        selection = input("Reverse Direction (Y)")
        reverse = False
        if (selection == "Y"):
            reverse = True
        xcord = 0
        ycord = 0


        selection = input("left(l) middle(m) right(r) or custom(c)")
        if (selection == "l"):
            xcord = 0
            ycord = 0
        if (selection == "m"):
            xcord = 800
            ycord = 0
        if (selection == "r"):
            xcord = 1600
            ycord = 0
        if (selection == "c"):
            xcord = input("xcord?")
            ycord = input("ycord?")
        if (not reverse):
            for x in range(numberOfEnemies):    
                enemies.append([time, typeOfEnemy, xcord, ycord, x+offset, row, path, speed])
                time += interval
        else:
            time += (numberOfEnemies-1)*interval
            for x in range(numberOfEnemies):    
                enemies.append([time, typeOfEnemy, xcord, ycord, x+offset, row, path, speed])
                time -= interval
            time += (numberOfEnemies+1)*interval
                
    elif (selection == "2"):
        print("time is currently ", time)
        time = int(input("What should time be changed to?"))

    elif (selection == "3"):
        #sort, write, and quit
        enemiesSorted = sorted(enemies)
        for x in enemiesSorted:
            f.write(str(x[0])+" "+str(x[1])+" "+str(x[2])+" "+str(x[3])+" "+str(x[4])+" "+str(x[5])+" "+str(x[6])+" "+str(x[7])+"\n")
        f.close()
        print(enemiesSorted)
        break

        
