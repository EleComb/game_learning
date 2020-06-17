

def print_text(screen, font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


def wrap_angle(angle):
    return angle % 360
