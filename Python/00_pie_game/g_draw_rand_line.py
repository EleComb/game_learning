import sys, random
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Drawing Lines")


screen.fill((0, 80, 0))


for i in range(1000):
    # draw the line
    color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    width = 2
    pygame.draw.line(screen, color, (random.randint(0, 600), random.randint(0, 500)), (random.randint(0, 600), random.randint(0, 500)), width)

while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    pygame.display.update()
