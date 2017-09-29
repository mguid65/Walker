#! /usr/bin/python3

from math import pi
import sys
import pygame
from pygame import *


WIN_WIDTH = 1920
WIN_HEIGHT = 1080
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 0


def main():

    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    up = down = left = right = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#ffffff"))
    entities = pygame.sprite.Group()
    walkentity = WalkEntity(32, 32)
    platforms = []

    x = -4096
    y = 0
    level = ["RGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRGRG"]
    # build the level
    for row in level:
        for col in row:
            if col == "R":
                p = Platform(x, y, "grey")
                platforms.append(p)
                entities.add(p)
            elif col == "G":
                p = Platform(x, y, "green")
                platforms.append(p)
                entities.add(p)
            x += 128
        #y += 32
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = 1080
    camera = Camera(simple_camera, total_level_width, total_level_height)
    entities.add(walkentity)
    running = True
    while running == True:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
       	    

        # draw background
        for y in range(64):
            for x in range(64):
                screen.blit(bg, (x * 32, y * 32))
        
        camera.update(walkentity)

        # update WalkEntity, draw everything else
        walkentity.update(up, down, left, right, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()
    pygame.quit()
    sys.exit()

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.left,1080-32)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+WIN_HEIGHT, w, h)



class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class WalkEntity(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#ffffff"))
        self.image.convert()
        self.rect = pygame.draw.circle(self.image, (255,0,0), (x-16,y-16),16)
        self.nodes = []
        self.nodes.append(self.rect)

    def update(self, up, down, left, right, platforms):

        # remove control code.
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions

        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    #def addnode(self):
        #implement
    #def addlink(self):
        #implement


class Platform(Entity):
    def __init__(self, x, y, color):
        Entity.__init__(self)
        self.image = Surface((128, 32))
        self.image.convert()
        if(color == "green"):
            self.image.fill(Color("#01ff01"))
        elif(color == "red"):
            self.image.fill(Color("#D3D3D3"))
        self.rect = Rect(x, y, 128, 32)

    def update(self):
        pass

if __name__ == "__main__":
    main()
