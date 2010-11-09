#!/usr/bin/env python

from singleton import *

import pygame as pg
from pygame.locals import *

class Graphics(Singleton):
    def __init__(self):
        # Set the caption for the display
        pg.display.set_caption('Super Sub')
        # Define the variable for the screen.
        self.screen = None
    
    # Set the resolution of the window.
    # res = (width, height)
    def set_res(self, res):
        # Create a screen with the specified resolution.
        self.screen = pg.display.set_mode(res)
    
    # Clear the screen.
    def clear(self):
        self.screen.fill(pg.Color("black"))
    
    # Flip the back-buffers, pushing all changes to the screen.
    def flip(self):
        pg.display.flip()
