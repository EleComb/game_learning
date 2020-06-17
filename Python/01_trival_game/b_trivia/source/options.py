import pygame

# main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("The Trivia Game")


font1 = pygame.font.Font(None, 40)
font2 = pygame.font.Font(None, 24)
white = 255, 255, 255
cyan = 0, 255, 255
yellow = 255, 255, 0
purple = 255, 0, 255
green = 0, 255, 0
red = 255, 0, 0


def print_text(font, x, y, text, color=(255, 255, 255), shadow=True):
    if shadow:
        imgText = font.render(text, True, (0, 0, 0))
        screen.blit(imgText, (x-2, y-2))
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

