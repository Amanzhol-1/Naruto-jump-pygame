import pygame
from pygame.locals import *
from random import randint
from config import *
#Базовый класс для спрайта
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        #Иницилизация
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
    def move_x(self, x):
        self.x = self.x + x
        self._move()
    
    def move_y(self, y):
        self.y = self.y + y
        self._move()
        
    def set_x(self, x):
        self.x = x
        self._move()
    
    def set_y(self, y):
        self.y = y
        self._move()
        
    def _move(self):
        self.rect.center = (self.x,self.y)


    #Инициализация изображения спрайта
    def init_image(self, imgPath):
        self.image = pygame.image.load(imgPath).convert()
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        

#Класс для енеми
class Monster(Sprite):
    def __init__(self, x,y):
        Sprite.__init__(self,x,y)
        self.init_image('img/monster.png')
    #Его движение
    def move(self):
        self.move_x(randint(-5, 5))
        self.move_y(randint(-5, 5))

#Класс для игрока
class Doodle(Sprite):
    name = "Anonymus"
    score = 0
    alive = 1
    ySpeed = 5
    x = doodle_start_position[0]
    y = doodle_start_position[1]
    def __init__(self, name):
        "�������������"
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.img_r = pygame.image.load('img/naruto.png').convert()
        self.img_l = pygame.transform.flip(self.img_r, True, False) 
        self.image = self.img_r
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
    #функция для движения игрока
    def _move(self):
        self.rect.center = (self.x,self.y)
        if self.y >= screen_height:
            self.alive = 0     
    #изменение хитбоксов при движении
    def get_legs_rect(self):
        left = self.rect.left + self.rect.width*0.1
        top = self.rect.top + self.rect.height*0.9
        width = self.rect.width*0.6
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
		
    
    def set_x(self, x):
        "�����, ��������������� ��������� ������� �� ��� X"
        if x < self.x:
            self.image = self.img_l
        elif x > self.x:
            self.image = self.img_r
        self.x = x
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self._move()
    
    def inc_y_speed(self, speed):
        "�����, ������������� �������� �������"
        self.ySpeed = self.ySpeed + speed
    
    def inc_score(self, score):
        self.score = self.score + score
        

#класс для платформ
class Platform(Sprite):

    def get_surface_rect(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
        #функция для появления платформ и для пружин появляющихся на них
    def __init__(self, x, y):
        Sprite.__init__(self, x, y)
        if type(self).__name__ == "Platform":
            self.init_image('img/greenplatform.png')
            rnd = randint(-100, 100)
            if rnd >= 0:
                self.spring = Spring(self.x+randint(-int(platform_width/2 - 10), int(platform_width/2) - 10), self.y-20)
            else:
                self.spring = None
            
        
#класс для движущихся платформ
class MovingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.init_image('img/blueplatform.png')    
        self.way = -1 
        self.xSpeed = randint(2, 6)
        self.spring = None
    #для их движения
    def move(self):
        self.move_x(self.xSpeed*self.way)
        if  10 < self.x < 19 or 460 < self.x < 469:
            self.way = - self.way
#для ломающихся платформ
class CrashingPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.init_image('img/brownplatform.png')
        self.ySpeed = 10
        self.crashed = 0
        self.spring = None
    #функция работает если они сломаны
    def crash(self):
        self.init_image('img/brownplatformbr.png')
        self.crashed = 1
    
    def move(self):
        if self.crashed == 0: #пока игрок не коснулся их, они находятся без изменений
            pass
        
        elif self.crashed == 1: #если игрок коснулся, то платформы ломаются
            self.move_y(self.ySpeed)
    def renew(self):
        Platform.renew(self)
        self.init_image('img/brownplatform.png')
        self.crashed = 0
# для деревьев
class Spring(Sprite):
    def __init__(self, x, y):
        self.x = x - 25
        self.y = y
        compressed = 0
        pygame.sprite.Sprite.__init__(self)

        self.init_image('img/spring.png')
    #Если игрок коснулся их, то деревья сжимаются
    def compress(self):
        self.init_image('img/spring_comp.png')
        self.compressed = 1
    #Если игрок запрыгнет на дерево, то он прыгает выше
    def get_top_surface(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)

#Класс для хитбоксы
class Rectangle(pygame.Surface):
    def __init__(self, width, heigth,color):
        pygame.Surface.__init__(self,(width, heigth), pygame.SRCALPHA)
        self.fill(color)
#Для тексты Score
class TextSprite(Sprite):
    def __init__(self, x, y, text='', size=35, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)  #загрузить шрифт по умолчанию, размер 25
        self.color = color         # цвет нашего шрифта
        self.text = text
        self.generateImage() #генерировать изображение
    #Текст
    def setText(self, text):
        self.text = text
        self.generateImage()
    #Цвет
    def setColor(self, color):
        self.color = color
        self.generateImage()
    #Размер
    def setSize(self, size):
        self.font = pygame.font.Font(None, size)
        self.generateImage()
    #Генерация изоброжения
    def generateImage(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)