import pygame
from pygame.locals import *
from sprites import Doodle, Platform, MovingPlatform,TextSprite, CrashingPlatform, Rectangle, Spring, Monster
from random import randint
import os
from config import *
os.chdir('C:/Users/acer/Desktop/git lessin/Naruto--main/Naruto jump')
#Класс для локации
class Location(object):
    parent = None
    def __init__(self, parent):
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.background = pygame.image.load('img/fone.jpg').convert()
    def event(self,event):
        pass
    def draw(self):
        pass

#Класс для формировании платформ, деревьев и енеми
class GameLocation(Location):
    
    def __init__(self, parent, name):
        Location.__init__(self, parent)
        pygame.key.set_repeat(10)
        pygame.mouse.set_visible(0)
        self.doodle = Doodle(name)
        self.doodle.name = name
        self.allsprites = pygame.sprite.Group()
        self.allsprites.add(self.doodle)
        for i in range(0, platform_count):
            self.allsprites.add(self.randomPlatform(False))
        for platform in self.allsprites:
            if isinstance(platform, Platform) and platform.spring != None:
                self.allsprites.add(platform.spring)

        self.score_sprite = TextSprite(50,25,self.doodle.name, 45, (0,0,0))
        self.allsprites.add(self.score_sprite)
        self.header = Rectangle(screen_width, 50, (0,191,255,128))
        self.window.blit(self.background, (0, 0))
        
        self.monster = None
    
    #функция для случайного появления платформ
    def randomPlatform(self,top = True):
        x = randint(0, screen_width - platform_width)
        bad_y = []
        for spr in self.allsprites:
            bad_y.append((spr.y-platform_y_padding, spr.y + platform_y_padding + spr.rect.height))
        
        good = 0
        while not good:
            if top:
               y = randint(-100, 50)
            else:
                y = randint(0, screen_height)
            good = 1
            for bad_y_item in bad_y:
                if bad_y_item[0] <= y <= bad_y_item[1]:
                    good = 0
                    break
            
        dig = randint(0, 100)
        if dig < 35:
            return MovingPlatform(x,y)
        elif dig >= 35 and dig < 50:
            return CrashingPlatform(x,y)
        else:
            return Platform(x,y)
    
    
    
    def draw(self):
        if self.doodle.alive == 1:
            #случайное место появления енеми
            if self.monster == None:
                case = randint(-1000,5)
                if case > 0:
                    self.monster = Monster(randint(0, screen_width), randint(-19, 19)) #килаура 
                    self.allsprites.add(self.monster)
                    self.monster.move()
            #В случае если игрок коснется енеми 
            else:
                self.monster.move()
                if self.doodle.rect.colliderect(self.monster.rect):
                    self.doodle.alive = 0
                if self.monster.y >= screen_height:
                    self.allsprites.remove(self.monster)
                    self.monster = None
                    
            self.allsprites.clear(self.window, self.background)
            
            #для работы и движения игрока
            mousePos = pygame.mouse.get_pos()
            self.doodle.inc_y_speed(-gravitation)
            if mouse_enabled:
                self.doodle.set_x(mousePos[0])
            else:
                if transparent_walls:
                    if self.doodle.x < 0:
                        self.doodle.set_x(screen_width)
                    elif self.doodle.x > screen_width:
                        self.doodle.set_x(0)
            self.doodle.move_y(-self.doodle.ySpeed)
            for spr in self.allsprites:
                #Если игрок над деревом
                if isinstance(spr, Spring) and self.doodle.get_legs_rect().colliderect(spr.get_top_surface()) and self.doodle.ySpeed <= 0:
                    spr.compress()
                    self.doodle.ySpeed = spring_speed
                
                #Если игрок над платформой
                if isinstance(spr, Platform) and self.doodle.get_legs_rect().colliderect(spr.get_surface_rect()) and self.doodle.ySpeed <= 0:
                    if isinstance(spr,CrashingPlatform):
                        spr.crash()
                        break
                    self.doodle.ySpeed = jump_speed
            
                if isinstance(spr, Platform):
                    #Обновление платформ
                    if spr.y >= screen_height:
                        self.allsprites.remove(spr)
                        platform = self.randomPlatform()
                        self.allsprites.add(platform)
                        if isinstance(platform, Platform) and platform.spring != None:
                            self.allsprites.add(platform.spring)

                
                #Для двигающихся и ломающихся платформ
                if isinstance(spr,MovingPlatform) or (isinstance(spr,CrashingPlatform) and spr.crashed == 1):
                    spr.move()
            
            #Перемещение всего мира   
            if self.doodle.y < horizont:
                self.doodle.inc_score(self.doodle.ySpeed)
                for spr in self.allsprites:
                    if not isinstance(spr, TextSprite):
                        spr.move_y(self.doodle.ySpeed)
            
            
            #нарисовать все на холсте
            self.allsprites.draw(self.window)
            self.score_sprite.setText("               %s,    %s" % (self.doodle.name, int(self.doodle.score/10)))
            self.window.blit(self.header, (0,0))
        else:
            #В случае проигрыша, начнется все заного
            self.parent.location = GameLocation(self.parent,self.doodle.name)
    #Функция для нажатия клавиш
    def event(self,event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.doodle.set_x(self.doodle.x - 5)
            elif event.key == K_RIGHT:
                self.doodle.set_x(self.doodle.x + 5)