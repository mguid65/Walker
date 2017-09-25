import pygame
from pygame import *

infinity = 10^8
screen_width=720
screen_height=480
screen=pygame.display.set_mode([screen_width,screen_height])
pygame.display.update()


red = (255,0,0)
green = (100,255,100)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
pygame.init()
done = 0
while not done:

	screen.fill(white)
	pygame.draw.rect(screen, green, (-540,380,2160,100),0)
	pygame.display.update()
	
