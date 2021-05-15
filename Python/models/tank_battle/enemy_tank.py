from models.tank_battle.tank import Tank
from _.MyLibrary import *


class EnemyTank(Tank):
    def __init__(self, tank_file="enemy_tank.png", turret_file="enemy_turret.png"):
        Tank.__init__(self, tank_file, turret_file)

    def update(self, ticks):
        self.turret.rotation = wrap_angle(self.rotation - 90)
        Tank.update(self, ticks)

    def draw(self, surface):
        Tank.draw(self, surface)



