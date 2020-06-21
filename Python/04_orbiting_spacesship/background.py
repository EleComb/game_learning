import sys, random, math, pygame
from pygame.locals import *

import _.utils as utils


class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getx(self):
        return self.__x

    def setx(self, x):
        self.__x = x

    x = property(getx, setx)

    def gety(self):
        return self.__y

    def sety(self, y):
        self.__y = y

    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ", Y:" + "{:.0f}".format(self.__y) + "}"


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Orbit Demo")
font = pygame.font.Font(None, 18)

space = pygame.image.load("space.png").convert_alpha()
planet = pygame.image.load("planet2.png").convert_alpha()
ship = pygame.image.load("ship.png").convert_alpha()
width, height = ship.get_size()
ship = pygame.transform.smoothscale(ship, (width//2, height//2))

radius = 250
angle = 0.0
pos = Point(0, 0)
old_pos = Point(0, 0)
speed = 0.1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_UP]:
        speed  += 0.01
    elif keys[K_DOWN]:
        speed -= 0.01

    screen.blit(space, (0, 0))

    width, height = planet.get_size()
    screen.blit(planet, (400 - width/2, 300 - height/2))

    # move the ship
    angle = utils.wrap_angle(angle - speed)
    pos.x = math.sin( math.radians(angle) ) * radius
    pos.y = math.cos( math.radians(angle) ) * radius

    # rotate the ship
    delta_x = ( pos.x - old_pos.x )
    delta_y = ( pos.y - old_pos.y )
    rangle = math.atan2(delta_y, delta_x)
    rangled = utils.wrap_angle( -math.degrees(rangle) )
    scratch_ship = pygame.transform.rotate(ship, rangled)

    # draw the ship
    width, height = scratch_ship.get_size()
    x = 400 + pos.x - width // 2
    y = 300 + pos.y - height // 2
    screen.blit(scratch_ship, (x, y))

    utils.print_text(screen, font, 0, 0, "Orbit: " + "{:.0f}".format(angle))
    utils.print_text(screen, font, 0, 20, "Rotation: " + "{:.2f}".format(angle))
    utils.print_text(screen, font, 0, 40, "Position: " + str(pos))
    utils.print_text(screen, font, 0, 60, "Old Pos: " + str(old_pos))

    pygame.display.update()

    # remember position
    old_pos.x = pos.x
    old_pos.y = pos.y