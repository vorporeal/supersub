#!/usr/bin/env python

import pygame as pg
from pygame.locals import *

from singleton import *

class Input(Singleton):
    def __init__(self):
        self.quit = False
        self.keys = Keys()
    
    def update(self):
        # Make sure keyboard and mouse data is up-to-date.
        pg.event.pump()
        
        # Loop through events, changing data as necessary.
        for evt in pg.event.get():
            if evt.type == KEYDOWN:
                self.keys.keydown(evt.key)
            if evt.type == KEYUP:
                self.keys.keyup(evt.key)
            if evt.type == QUIT:
                self.quit = True
        
        # Handle globally defined input also.
        if K_ESCAPE in self.keys.pressed:
            self.quit = True

# This class is a singleton that can be requested to get access to
# unbuffered input data.
class Keys(Singleton):
    def __init__(self):
        self.pressed = {}
    
    def keydown(self, key):
        self.pressed[key] = True
    
    def keyup(self, key):
        if key in self.pressed:
            del self.pressed[key]