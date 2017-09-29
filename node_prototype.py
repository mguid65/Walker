import pygame
from pygame import *

nodes = []
muscles = []
platforms = []


class Node():
    def __init__(self,x,y):
        self.xvelocity = 0
        self.yvelocity = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#ffffff"))
        self.image.convert()
        self.rect = pygame.draw.circle(self.image, (255,0,0),(x-16,y-16),16)

    def update(self,muscle_extend, addxvel, addyvel):
        if (muscle_extend == True)
            self.xvelocity += addxvel
            self.yvelocity += addyvel
        if not self.onGround:
            self.yvelocity +=0.3
            if self.yvelocity > 100: 
                self.yveocity = 100
        self.rect.left += self.xvelocity
        self.rect.top += self.yvelocity
        self.onGround = False;
        self.collide(0, self.yvelocity, platforms)
        

    def collide(self,yvelocity):
        for p in platforms:
            if pygame.sprite.collide_rect(self,p):
                if yvelocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvelocity < 0:
                    self.rect.top = p.rect.bottom

class Muscle()
    
