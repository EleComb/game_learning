import sys, time, random, math, pygame
from pygame.locals import *
from _.MyLibrary import *


class SnakeSegment(MySprite):
    def __init__(self, color=(20, 200, 20)):
        global size_rate
        MySprite.__init__(self)
        image = pygame.Surface((32*size_rate, 32*size_rate)).convert_alpha()
        image.fill((255, 255, 255, 0))
        pygame.draw.circle(image, color, (16*size_rate, 16*size_rate), 16*size_rate, 0)
        self.set_image(image)
        MySprite.update(self, 0, 30)  # create frame image


class Snake():
    global size_rate

    def __init__(self):
        self.velocity = Point(-1, 0)
        self.old_time = 0
        head = SnakeSegment((50, 250, 50))
        head.X = 12 * 32*size_rate
        head.Y = 9 * 32*size_rate
        self.segments = list()
        self.segments.append(head)
        self.add_segment()
        self.add_segment()

    def update(self, ticks):
        global step_time, head_x, head_y
        head_x = self.segments[0].X // (32*size_rate)
        head_y = self.segments[0].Y // (32*size_rate)
        if ticks > self.old_time + step_time:
            self.old_time = ticks

            # move body segments
            for n in range(len(self.segments) - 1, 0, -1):
                self.segments[n].X = self.segments[n - 1].X
                self.segments[n].Y = self.segments[n - 1].Y

            # move snake head
            self.segments[0].X += self.velocity.x * (32*size_rate)
            self.segments[0].Y += self.velocity.y * (32*size_rate)

    def draw(self, surface):
        for segment in self.segments:
            surface.blit(segment.image, (segment.X, segment.Y))

    def add_segment(self):
        last = len(self.segments) - 1
        segment = SnakeSegment((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        start = Point(0, 0)
        if self.velocity.x < 0:
            start.x = (32*size_rate)
        elif self.velocity.x > 0:
            start.x = -(32*size_rate)
        if self.velocity.y < 0:
            start.y = (32*size_rate)
        elif self.velocity.y > 0:
            start.y = -(32*size_rate)
        segment.X = self.segments[last].X + start.x
        segment.Y = self.segments[last].Y + start.y
        self.segments.append(segment)


class Food(MySprite):
    def __init__(self):
        global size_rate
        MySprite.__init__(self)
        image = pygame.Surface(((32*size_rate), (32*size_rate))).convert_alpha()
        image.fill((255, 255, 255, 0))
        pygame.draw.circle(image, (250, 250, 50), (16*size_rate, 16*size_rate), 16*size_rate, 0)
        self.set_image(image)
        MySprite.update(self, 0, 30)
        self.X = random.randint(0, 23) * 32
        self.Y = random.randint(0, 17) * 32


def game_init():
    global screen, backbuffer, font, timer, snake, food_group, size_rate
    pygame.init()
    screen = pygame.display.set_mode((24 * 32, 18 * 32))
    pygame.display.set_caption("Snake Game")
    font = pygame.font.Font(None, 30)
    timer = pygame.time.Clock()

    # create a drawing surface
    backbuffer = pygame.Surface((screen.get_rect().width, screen.get_rect().height))

    # create snake
    snake = Snake()
    image = pygame.Surface((60, 60)).convert_alpha()
    image.fill((255, 255, 255, 0))
    pygame.draw.circle(image, (80, 80, 220, 70), ((32*size_rate)-2, (32*size_rate)-2), 30, 0)
    pygame.draw.circle(image, (80, 80, 250, 255), ((32*size_rate)-2, (32*size_rate)-2), (32*size_rate)-2, 4)

    # create food
    food_group = pygame.sprite.Group()
    food = Food()
    food_group.add(food)
    food = Food()
    food_group.add(food)
    food = Food()
    food_group.add(food)


def auto_move():
    direction = get_current_direction()
    food_dir = get_food_direction()
    if food_dir == "left":
        if direction != "right":
            direction = "left"
    elif food_dir == "right":
        if direction != "left":
            direction = "right"
    elif food_dir == "up":
        if direction != "down":
            direction = "up"
    elif food_dir == "down":
        if direction != "up":
            direction = "down"

    # set velocity based on direction
    if direction == "up":
        snake.velocity = Point(0, -1)
    elif direction == "down":
        snake.velocity = Point(0, 1)
    elif direction == "left":
        snake.velocity = Point(-1, 0)
    elif direction == "right":
        snake.velocity = Point(1, 0)


def get_current_direction():
    global head_x, head_y
    first_segment_x = snake.segments[1].X // (32 * size_rate)
    first_segment_y = snake.segments[1].Y // (32 * size_rate)
    if head_x - 1 == first_segment_x:
        return "right"
    elif head_x + 1 == first_segment_x:
        return "left"
    elif head_y - 1 == first_segment_y:
        return "down"
    elif head_y + 1 == first_segment_y:
        return "up"


def get_food_direction():
    global head_x, head_y
    food = Point(0, 0)
    for obj in food_group:
        food = Point(obj.X // (32 * size_rate), obj.Y // (32 * size_rate))
    if head_x < food.x:
        return "right"
    elif head_x > food.x:
        return "left"
    elif head_x == food.x:
        if head_y < food.y:
            return "down"
        elif head_y > food.y:
            return "up"


# main program begins
size_rate = 0.5
game_init()
game_over = False
last_time = 0
auto_play = False
step_time = 400


while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    # event section
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_SPACE]:
        if auto_play:
            auto_play = False
            step_time = 400
        else:
            auto_play = True
            step_time = 50
    elif keys[K_UP] or keys[K_w]:
        snake.velocity = Point(0, -1)
    elif keys[K_DOWN] or keys[K_s]:
        snake.velocity = Point(0, 1)
    elif keys[K_LEFT] or keys[K_a]:
        snake.velocity = Point(-1, 0)
    elif keys[K_RIGHT] or keys[K_d]:
        snake.velocity = Point(1, 0)

    # update section
    if not game_over:
        snake.update(ticks)
        food_group.update(ticks)
        # try to pick up food
        hit_list = pygame.sprite.groupcollide(snake.segments, food_group, False, True)
        if len(hit_list) > 0:
            food_group.add(Food())
            snake.add_segment()

    # see if head collides with body
    for n in range(1, len(snake.segments)):
        if pygame.sprite.collide_rect(snake.segments[0], snake.segments[n]):
            game_over = True

    # check screen boundary
    x = snake.segments[0].X // (32 * size_rate)
    y = snake.segments[0].Y // (32 * size_rate)
    if x < 0 or x > 24/size_rate or y < 0 or y > 17/size_rate:
        game_over = True

    # draw section
    backbuffer.fill((20, 50, 20))
    snake.draw(backbuffer)
    food_group.draw(backbuffer)
    screen.blit(backbuffer, (0, 0))

    if not game_over:
        if auto_play:
            auto_move()
        print_text(font, 0, 0, "Length " + str(len(snake.segments)))
        print_text(font, 0, 20, "Position " + str(snake.segments[0].X // (32 * size_rate)) +
                   "," + str(snake.segments[0].Y // (32 * size_rate)))
        print_text(font, 0, 40, "head:" + str(head_x) + "," + str(head_y))
    else:
        print_text(font, 0, 0, "GAME OVER")

    pygame.display.update()

