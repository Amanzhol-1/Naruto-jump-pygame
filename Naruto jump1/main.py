#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
# _view for exe building
#from pygame import _view
from pygame.locals import *
import sys
import os
from locations import *
from sprites import *
from config import screen_width, screen_height, fps
os.chdir('C:/Users/acer/Desktop/git lessin/Naruto--main/Naruto jump')
#Чтобы музыка играла все время игры
pygame.mixer.init()
pygame.mixer.music.load('C:/Users/acer/Desktop/git lessin/Naruto--main/Naruto jump/img/M.mp3')
pygame.mixer.music.play(-1) 
#Параметры окна для игры
class Game():

    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Naruto Jump')
    def event(self, event):
        if event.type == QUIT:
            sys.exit()
                

#главная функция через которую работает вся игра
def main():
    game = Game()
    game.location = GameLocation(game,'Score')
    clock = pygame.time.Clock()
    while 1:
        clock.tick(fps)
        game.location.draw()
        pygame.display.flip()
        for event in pygame.event.get():
           game.location.event(event)
           game.event(event)            
            
    
if __name__ == "__main__":
    main()
