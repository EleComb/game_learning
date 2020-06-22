import sys, time, random, math, pygame
from pygame.locals import *
import _.utils as utils


class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    def _getpos(self): return self.rect.topleft
    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
            "," + str(self.last_frame) + "," + str(self.frame_width) + \
            "," + str(self.frame_height) + "," + str(self.columns) + \
            "," + str(self.rect)


def reset_arrow():
    y = random.randint(250, 350)
    arrow.position = 800, y


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape The Dragon Game")
font = pygame.font.Font(None, 18)
framerate = pygame.time.Clock()

bg = pygame.image.load("space.png").convert_alpha()

group = pygame.sprite.Group()

dragon = MySprite(screen)
dragon.load("dragon.png", 260, 150, 3)
dragon.position = 100, 230
group.add(dragon)

player = MySprite(screen)
player.load("caveman.png", 50, 64, 8)
player.first_frame = 1
player.last_frame = 7
player.position = 400, 303
group.add(player)

arrow = MySprite(screen)
arrow.load("flame.png", 40, 16, 1)
arrow.position = 800, 320
group.add(arrow)

arrow_vel = 8.0
game_over = False
you_win = False
player_jumping = False
jump_vel = 0.0
player_start_y = player.Y

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        sys.exit()
    elif key[K_SPACE]:
        if not player_jumping:
            player_jumping = True
        jump_vel = -8.0
    elif key[K_q]:
        arrow_vel = 8.0
        game_over = False
        you_win = False
        player_jumping = False
        jump_vel = 0.0
        player_start_y = player.Y
        dragon.position = 100, 230
        player.position = 400, 303

    if not game_over:
        arrow.X -= arrow_vel

    if pygame.sprite.collide_rect(arrow, player):
        reset_arrow()
        player.X -= 10

    if pygame.sprite.collide_rect(arrow, dragon):
        reset_arrow()
        dragon.X -= 10

    if pygame.sprite.collide_rect(player, dragon):
        game_over = True

    if dragon.X < -100:
        you_win = True
        game_over = True

    if player_jumping:
        player.Y += jump_vel
        jump_vel += 0.5
        if player.Y > player_start_y:
            player_jumping = False
            player.Y = player_start_y
            jump_vel = 0.0

    screen.blit(bg, (0, 0))
    if not game_over:
        group.update(ticks, 30)

    group.draw(screen)

    utils.print_text(screen, font, 0, 0, "player.Y: " + str(player.Y))
    utils.print_text(screen, font, 0, 15, "player_start_y: " + str(player_start_y))
    utils.print_text(screen, font, 0, 30, "player_jumping: " + str(player_jumping))
    utils.print_text(screen, font, 350, 560, "Press SPACE to jump!")

    if game_over:
        utils.print_text(screen, font, 360, 100, "G A M E  O V E R, PRESS Q TO RESTART")
        if you_win:
            utils.print_text(screen, font, 330, 130, "YOU BEAT THE DRAGON! PRESS Q TO RESTART")
        else:
            utils.print_text(screen, font, 330, 130, "THE DRAGON GOT YOU! PRESS Q TO RESTART")

    pygame.display.update()
