import sys
from pygame.locals import *
from ab_trival_game.b_trivia.source.trivia import Trivia
from ab_trival_game.b_trivia.source.options import *


# load the trivia data file
trivia2 = Trivia("source\\trivia_data.txt")

# repeating loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key ==pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                trivia2.handle_input(1)
            elif event.key == pygame.K_2:
                trivia2.handle_input(2)
            elif event.key == pygame.K_3:
                trivia2.handle_input(3)
            elif event.key == pygame.K_4:
                trivia2.handle_input(4)
            elif event.key == pygame.K_RETURN:
                trivia2.next_question()

    # clear the screen
    screen.fill((0, 0, 200))

    # display trivia data
    trivia2.show_question()

    # update the display
    pygame.display.update()
