import pygame as pg
import writetocsv
import time

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


def fixat(trialnum, fixnum, logfile):
    pg.init()

    info = pg.display.Info()
    # screen = pg.display.set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
    screen = pg.display.set_mode((info.current_w, info.current_h), pg.RESIZABLE)

    screen_rect = screen.get_rect()
    font = pg.font.Font(None, 750)
    clock = pg.time.Clock()
    # countnum += 1
    txt = font.render('.', True, WHITE)
    txttocsv = 'Fixation Start trial number {0} fixture number {1}'.format(trialnum, fixnum)
    writetocsv.writelogcsv(txttocsv, logfile)
    if trialnum == 1 and fixnum == 1:
        t_end = time.time() + 60
    else:
        t_end = time.time() + 30
    while time.time() < t_end:
        screen.blit(txt, txt.get_rect(center=screen_rect.center))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True
                    pg.quit()

    txttocsv = 'Fixation End Number {0}'.format(trialnum)
    writetocsv.writelogcsv(txttocsv, logfile)

    pg.quit()
