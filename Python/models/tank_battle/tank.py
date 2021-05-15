from _.MyLibrary import *


class Tank(MySprite):
    def __init__(self, tank_file="tank.png", turret_file="turret.png"):
        MySprite.__init__(self)
        self.load(tank_file, 50, 60, 4)
        self.speed = 0.0
        self.scratch = None
        self.float_pos = Point(0, 0)
        self.velocity = Point(0, 0)
        self.turret = MySprite()
        self.turret.load(turret_file, 32, 64, 4)
        self.fire_timer = 0
        self.rotation = 0

    def update(self, ticks):
        # update chassis
        MySprite.update(self, ticks, 100)
        self.rotation = wrap_angle(self.rotation)
        self.scratch = pygame.transform.rotate(self.image, -self.rotation)
        angle = wrap_angle(self.rotation - 90)
        self.velocity = angular_velocity(angle)
        self.float_pos.x += self.velocity.x
        self.float_pos.y += self.velocity.y

        # warp tank around screen edges (keep it simple)
        if self.float_pos.x < -50:
            self.float_pos.x = 800
        elif self.float_pos.x > 800:
            self.float_pos.x = -50
        if self.float_pos.y < -60:
            self.float_pos.y = 600
        elif self.float_pos.y > 600:
            self.float_pos.y = -60

        # transfer float position to integer position for drawing
        self.X = int(self.float_pos.x)
        self.Y = int(self.float_pos.y)

        # update turret
        self.turret.position = (self.X, self.Y)
        self.turret.last_frame = 0
        self.turret.update(ticks, 100)
        self.turret.rotation = wrap_angle(self.turret.rotation)
        angle = self.turret.rotation + 90
        self.turret.scratch = pygame.transform.rotate(self.turret.image, -angle)

    def draw(self, surface):
        # draw the chassis
        width, height = self.scratch.get_size()
        center = Point(width / 2, height / 2)
        surface.blit(self.scratch, (self.X - center.x, self.Y - center.y))
        # draw the turret
        width, height = self.turret.scratch.get_size()
        center = Point(width / 2, height / 2)
        surface.blit(self.turret.scratch, (self.turret.X - center.x, self.turret.Y - center.y))

    def __str__(self):
        return MySprite.__str__(self) + "," + str(self.velocity)


