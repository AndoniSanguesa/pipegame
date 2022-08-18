import pygame as pg
from pygame import freetype
from element import Element
from graph import Graph
from win_screen import WinScreen

width, height = (1800, 1000)
screen = pg.display.set_mode((width, height))


freetype.init(resolution=150)

font = freetype.SysFont(freetype.get_default_font(), 25)

done = False

clock = pg.time.Clock()

Graph(screen, font, (10,6))
WinScreen(screen, font)

while not done:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        for item in Element.element_dict.values():
            item.event(event)
        if event.type == pg.QUIT:
            done = True

    for item in Element.element_dict.values():
        item.draw()

    pg.display.flip()
    clock.tick(60)