import pygame
import sys

from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Drawing Ellipse")

while True:

    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    screen.fill((0, 0, 255))

    # draw a ellipse
    color = 255, 255, 0
    width = 10
    rect = 100, 50, 300, 250
    pygame.draw.ellipse(screen, color, rect, width)

    pygame.display.update()
