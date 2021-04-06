from _.MyLibrary import *


def calc_velocity(direction, vel=1.0):
    velocity = Point(0, 0)
    if direction == 0: # north
        velocity.y = -vel
    elif direction == 2: # east
        velocity.x = vel
    elif direction == 4: # south
        velocity.y = vel
    elif direction == 6: # west
        velocity.x = -vel
    return velocity


def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision Demo")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()

player_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

player = MySprite()
player.load("player.png", 96, 96, 8)
player.position = 80, 80
player.direction = 4
player_group.add(player)

for n in range(0, 5):
    zombie = MySprite()
    zombie.load("zombie.png", 96, 96, 8)
    zombie.position = random.randint(0, 700), random.randint(0, 500)
    zombie.direction = random.randint(0, 3) * 2
    zombie_group.add(zombie)


# create health sprite
for n in range(0, 3):
    health = MySprite()
    health.load("health.png", 32, 32, 1)
    health.position = random.randint(0, 700), random.randint(0, 500)
    health_group.add(health)

game_over = False
player_moving = False
player_health = 100

ticks_lock = 0
zombie_group_tmp = zombie_group.copy()
# repeating loop
while True:

    timer.tick(30)
    ticks = pygame.time.get_ticks()
    if int(ticks/1000) % 5 == 0 and int(ticks/1000) is not ticks_lock:
        zombie = MySprite()
        zombie.load("zombie.png", 96, 96, 8)
        zombie.position = random.randint(0, 700), random.randint(0, 500)
        zombie.direction = random.randint(0, 3) * 2
        zombie_group.add(zombie)
        zombie_group_tmp = zombie_group.copy()
        ticks_lock = int(ticks/1000)

    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]: sys.exit()
    elif keys[K_UP] or keys[K_w]:
        player.direction = 0
        player_moving = True
    elif keys[K_RIGHT] or keys[K_d]:
        player.direction = 2
        player_moving = True
    elif keys[K_DOWN] or keys[K_s]:
        player.direction = 4
        player_moving = True
    elif keys[K_LEFT] or keys[K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False

    # these things should not happen when the game is over

    if not game_over:
        # set animation frames based on player's direction
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns - 1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        if not player_moving:
            # stop animating when player is not pressing a key
            player.frame = player.first_frame = player.last_frame
        else:
            # move player in direction
            player.velocity = calc_velocity(player.direction, 5)
            player.velocity.x *= 1.5
            player.velocity.y *= 1.5

        # update player sprite
        player_group.update(ticks, 50)

        # manually move the player
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y
            if player.X < 0: player.X = 0
            elif player.X > 700: player.X = 700
            if player.Y < 0: player.Y = 0
            elif player.Y > 500: player.Y = 500

        # update zombie sprites
        zombie_group.update(ticks, 50)

        # manually iterate through all the zombies
        for z in zombie_group:
            # set the zombie's animation range
            z.first_frame = z.direction * z.columns
            z.last_frame = z.first_frame + z.columns - 1
            if z.frame < z.first_frame:
                z.frame = z.first_frame
            z.velocity = calc_velocity(z.direction, vel=3)

            # keep the zombie on the screen
            z.X += z.velocity.x
            z.Y += z.velocity.y
            if z.X < 0 or z.X > 700 or z.Y < 0 or z.Y > 500:
                reverse_direction(z)

        # check for collision with zombies
        attacker = pygame.sprite.spritecollideany(player, zombie_group)

        if attacker is not None:
            # we got a hit, now do a more precise check
            if pygame.sprite.collide_rect_ratio(0.5)(player, attacker):
                player_health -= 10
                if attacker.X < player.X:
                    attacker.X -= 10
                elif attacker.X > player.X:
                    attacker.X += 10
            else:
                attacker = None

        # zombie collision
        # Not Good Performance
        # zombie_group_tmp = zombie_group.copy()
        for one_zombie in zombie_group.spritedict:
            zombie_group_tmp.remove(one_zombie)
            zombie_collision = pygame.sprite.spritecollideany(one_zombie, zombie_group_tmp)
            if zombie_collision is not None:
                if pygame.sprite.collide_rect_ratio(0.5)(one_zombie, zombie_collision):
                    if zombie_collision.X < one_zombie.X:
                        reverse_direction(one_zombie)
                        zombie_collision.X -= 10
                        reverse_direction(zombie_collision)
                    elif zombie_collision.X > one_zombie.X:
                        zombie_collision.X += 10
                        reverse_direction(one_zombie)
                        reverse_direction(zombie_collision)
            zombie_group_tmp.add(one_zombie)

        # update the health drop
        health_group.update(ticks, 50)

        for health in health_group:
            # check for collision with health
            if pygame.sprite.collide_rect_ratio(0.5)(player, health):
                player_health += 30
                if player_health > 100: player_health = 100
                health.X = random.randint(0, 700)
                health.Y = random.randint(0, 500)

        # is player dead?
        if player_health <= 0:
            game_over = True

        # clear the screen
        screen.fill((50, 50, 100))

        # draw sprites
        health_group.draw(screen)
        zombie_group.draw(screen)
        player_group.draw(screen)

        # draw energy bar
        pygame.draw.rect(screen, (50, 150, 50, 180), Rect(300, 570, player_health*2, 25))
        pygame.draw.rect(screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 2)

        if game_over:
            print_text(font, 300, 100, "G A M E O V E R")

        pygame.display.update()



















