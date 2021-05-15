import sys, time, random, math, pygame
from pygame.locals import *
from _.MyLibrary import *
from models.tank_battle.tank import Tank
from models.tank_battle.enemy_tank import EnemyTank
from models.tank_battle.bullet import Bullet


def fire_canno(tank):
    position = Point(tank.turret.X, tank.turret.Y)
    bullet = Bullet(position)
    angle = tank.turret.rotation
    bullet.velocity = angular_velocity(angle)
    bullets.append(bullet)
    play_sound(shoot_sound)
    return bullet


def player_fire_cannon():
    bullet = fire_canno(player)
    bullet.owner = "player"
    bullet.color = (30, 250, 30)


def enemy_fire_cannon():
    bullet = fire_canno(enemy_tank)
    bullet.owner = "enemy"
    bullet.color = (250, 30, 30)


def game_init():
    global screen, backbuffer, font, timer, player_group, player, \
        enemy_tank, bullets, crosshair, crosshair_group

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    backbuffer = pygame.Surface((800, 600))
    pygame.display.set_caption("Tank Battle Game")
    font = pygame.font.Font(None, 30)
    timer = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    # load mouse cursor
    crosshair = MySprite()
    crosshair.load("crosshair.png")
    crosshair_group = pygame.sprite.GroupSingle()
    crosshair_group.add(crosshair)

    # create player tank
    player = Tank()
    player.float_pos = Point(400, 300)

    # create enemy tanks
    enemy_tank = EnemyTank()
    enemy_tank.float_pos = Point(random.randint(50, 760), 50)
    enemy_tank.rotation = 135

    # create bullets
    bullets = list()


def audio_init():
    global shoot_sound, boom_sound

    pygame.mixer.init()

    # load sound files
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    boom_sound = pygame.mixer.Sound("boom.wav")

    # this function uses any avaliable channel to play a sound clip


def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)


# main program begins
game_init()
audio_init()
game_over = False
player_score = 0
enemy_score = 0
last_time = 0
mouse_x = mouse_y = 0

while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    # reset mouse state variables
    mouse_up = mouse_down = 0
    mouse_up_x = mouse_up_y = 0
    mouse_down_x = mouse_down_y = 0

    # event section
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            move_x, move_y = event.rel
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = event.button
            mouse_down_x, mouse_down_y = event.pos
        elif event.type == MOUSEBUTTONUP:
            mouse_up = event.button
            mouse_up_x, mouse_up_y = event.pos

    # get key states
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_LEFT] or keys[K_a]:
        player.rotation -= 2.0
    elif keys[K_RIGHT] or keys[K_d]:
        player.rotation += 2.0

    # fire cannon
    if keys[K_SPACE] or mouse_up > 0:
        if ticks > player.fire_timer + 1000:
            player.fire_timer = ticks
            player_fire_cannon()

    # update section
    if not game_over:
        crosshair.position = (mouse_x, mouse_y)
        crosshair_group.update(ticks)

        # point tank turret toward crosshair
        angle = target_angle(player.turret.X, player.turret.Y,
            crosshair.X + crosshair.frame_width / 2,
            crosshair.Y + crosshair.frame_height / 2)
        player.turret.rotation = angle

        # move tank
        player.update(ticks)

        # update enemies
        enemy_tank.update(ticks)
        if ticks > enemy_tank.fire_timer + 1000:
            enemy_tank.fire_timer = ticks
            enemy_fire_cannon()

        # update bullets
        for bullet in bullets:
            bullet.update(ticks)
            if bullet.owner == "player":
                if pygame.sprite.collide_rect(bullet, enemy_tank):
                    player_score += 1
                    bullet.alive = False
                    play_sound(boom_sound)
                elif bullet.owner == "enemy":
                    if pygame.sprite.collide_rect(bullet, player):
                        enemy_score += 1
                        bullet.alive = False
                        play_sound(boom_sound)

    # drawing section
    backbuffer.fill((100, 100, 20))

    for bullet in bullets:
        bullet.draw(backbuffer)
    enemy_tank.draw(backbuffer)
    player.draw(backbuffer)
    crosshair_group.draw(backbuffer)

    screen.blit(backbuffer, (0, 0))

    if not game_over:
        print_text(font, 0, 0, "PLAYER " + str(player_score))
        print_text(font, 700, 0, "ENEMY " + str(enemy_score))
    else:
        print_text(font, 0, 0, "GAME OVER")

    pygame.display.update()

    # remove expired bulets
    for bullet in bullets:
        if not bullet.alive:
            bullets.remove(bullet)







