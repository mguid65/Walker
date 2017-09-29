# Matthew Guidry
# 29 September 2017
# Creature components
#
#


import pygame
from pygame import *

nodes = []
muscles = []
platforms = []

class Node():
    def __init__(self,tx,ty):
        self.friction = .01
        self.x = tx
        self.y = ty
        self.speed = 0
        self.angle = 0
        self.pfriction #previous friction
        self.px = self.x #previous x
        self.py = self.y #previous y
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#ffffff"))
        self.image.convert()
        self.rect = pygame.draw.circle(self.image, (255,0,0),(tx-16,ty-16),16)
    
    def update(self,muscle_state,newx,newy):
        if (muscle_state == True):
            self.x += math.sin(self.angle) * self.speed
            self.y -= math.cos(self.angle) * self.speed        
            return (self.x,self.y)
        else:
            self.x = newx
            self.y = newy
            
    def collide(self):
        for p in platforms:
            if pygame.sprite.collide_rect(self,p):
                if self.y >= p.top:
                    self.y = p.top+16
                    self.angle = math.pi - self.angle
                    onGround = True
                    
    def addVectors(coord1, coord2):
        angle1, length1 = coord1
        angle1, length1 = coord1
        
        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        angle  = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)
    
        return (angle, length)
    
    def accelerate(self, vector):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), vector)
    
    def modifyNode(self, mutability):
        # Previous values are for rolling back. Rolling back is 
        # useful in case a mutation doees nothing or worsens result.
        # Each node remembers its previous state.
        self.pfriction   #previous friction
        self.px = self.x #previous x
        self.py = self.y #previous y        
        self.x += mutability
        self.y += mutability
        self.friction += mutability
        
    def rollbackNode(self):
        self.friction = self.pfriction
        self.x = self.px
        self.y = self.py
    
class Muscle():
    def __init__(self,node1,node2,tcontractTime,tcontractLength, textendTime, textendLength):
        self.node1 = node1
        self.node2 = node2
        self.contracting = True
        self.contractTime = tcontractTime
        self.prev_ct = self.contractTime
        self.extendTime = textendTime
        self.prev_et = self.extendTime
        ##self.contractLength = tcontractLength
        ##self.extendLength = textendLength
        self.count=0
        self.timer=0
        pygame.draw.aaline(screen, (0,0,0), (int(node1.x), int(node1.y)), (int(node2.x), int(node2.y)))
        
        
        # let the time determine the extend and contract length
    def update(self):
        if self.contractTime == self.count and self.contracting == True:
            self.contracting = False
            self.count=0
        if self.extendTime == self.count and self.contrafting == False:
            self.contracting = True
            self.count=0
        
        # could probably do muscle extension a better way
        if self.contracting == True:
            self.node1.x -=2
            self.node1.y -=2
        if self.contracting == True:
            self.node1.x +=2
            self.node1.y +=2
        self.count+=1   
        
        # if a node is touching the ground, and muscle at the end of the extenstion, the force should be applied
        if((node1.onGround or node2.onGround) and self.count == self.extendTime):
            dx = self.node1.x - self.node2.x
            dy = self.node1.y - self.node2.y
            dist = math.hypot(dx, dy)
            theta = math.atan2(dy, dx)
            force = (self.extendLength - self.contractLength) * .5
            
            self.node1.accelerate((theta + 0.5 * math.pi, force))
            self.node2.accelerate((theta + 0.5 * math.pi, force))
                                  
            self.node1.update(True)
            self.node2.update(True)
        
    def modifyMuscle(self, mutability):
        self.prev_et = self.extendTime
        self.prev_ct = self.contractTime
        self.contractTime+=mutability
        self.extendTime+=mutability
        
    def rollbackMuscle(self):
        self.extendTime = self.prev_et
        self.contractTime = self.prev_ct
        
        
        
        
        
        
        
        
