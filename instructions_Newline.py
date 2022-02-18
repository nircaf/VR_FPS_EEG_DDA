from pygame.locals import *
import time
import pygame as pg
from itertools import chain
import mouse_mover
import ctypes
from ctypes import wintypes

def blit_text(surface, text, pos, font, color=pg.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def instructions(txt, *args):
    pg.init()
    info = pg.display.Info()
    WINDOWWIDTH = info.current_w
    WINDOWHEIGHT = info.current_h
    #                R    G    B
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BRIGHTRED = (255, 0, 0)
    RED = (155, 0, 0)
    BRIGHTGREEN = (0, 255, 0)
    GREEN = (0, 155, 0)
    BRIGHTBLUE = (0, 0, 255)
    BLUE = (0, 0, 155)
    BRIGHTYELLOW = (255, 255, 0)
    YELLOW = (155, 155, 0)
    DARKGRAY = (40, 40, 40)
    bgColor = BLACK

    screen = pg.display.set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
    screen_rect = screen.get_rect()
    font = pg.font.Font(None, 100)
    clock = pg.time.Clock()
    done = False
    # t_end = {'waldo': 20, 'space': 2000, 60:60, 10:10}
    if args[0] == 'space':
        t_end = time.time() + 2000
    else:
        t_end = time.time() + args[0]
    hwnd = pg.display.get_wm_info()['window']
    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT,
                                    wintypes.INT, wintypes.UINT]
    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)
    clicked = False
    while time.time() < t_end and not done:
        blit_text(screen, txt, (WINDOWWIDTH / 8, WINDOWHEIGHT / 12), font, WHITE)
        # screen.blit(txt, txt.get_rect(center=screen_rect.center))
        pg.display.flip()
        if not clicked:
            mouse_mover.click_mouse()
            clicked  = True
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                    return "abort"
                    # quit()
                elif event.key == pg.K_SPACE and args[0] == 'space':
                    done = True

    if args[0] == 60:
        pg.init()
        BEEP1 = pg.mixer.Sound('good_beep.wav')
        BEEP1.play()
        time.sleep(1)
        print("close eyes ended")
    pg.quit()


