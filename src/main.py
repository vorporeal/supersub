#!/usr/bin/env python

from graphics import *
import pygame as pg
from pygame.locals import *

def main():
    # Initialize pygame
    pg.init()
    
    # Make a variable to keep track of whether the game is running or stopped.
    running = True
    
    # Create our graphics manager.
    g = Graphics()
    g.set_res((640, 480))
    
    # A simple loop.  Doesn't handle quitting or anything.
    while(running):
        g.clear()
        pg.draw.circle(g.screen, pg.Color("cornflower blue"), (320, 240), 12)
        g.flip()

if __name__ == "__main__":
    main()