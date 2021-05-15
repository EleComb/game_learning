from models.tank_battle.tank import Tank
from _.MyLibrary import *


class Bullet():
    def __init__(self, position):
        self.alive = True
        self.color = (250, 20, 20)
        self.position = Point(position.x, position.y)
        self.velocity = Point(0, 0)
        self.rect = Rect(0, 0, 4, 4)
        self.owner = ""

    def update(self, ticks):
        self.position.x += self.velocity.x * 10.0
        self.position.y += self.velocity.y * 10.0
        if self.position.x < 0 or self.position.x > 800 \
                or self.position.y < 0 or self.position.y > 600:
            self.alive = False
        self.rect = Rect(self.position.x, self.position.y, 4, 4)

    def draw(self, surface):
        pos = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, self.color, pos, 4, 0)










