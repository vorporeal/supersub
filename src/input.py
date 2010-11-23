#!/usr/bin/env python

import pygame as pg
from pygame.locals import *

from singleton import *

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

class Mouse(Singleton):
    def __init__(self):
        self.pos = (0, 0)
        self.rel = (0, 0)
        self.clicked = []
        self.released = []
        self.down = []
    
    def update(self):
        self.clicked = []
        self.released = []
    
    def mouse_moved(self, pos, rel):
        self.pos = pos
        self.rel = rel
    
    def mouse_down(self, button):
        self.clicked.append(button)
        self.down.append(button)
    
    def mouse_up(self, button):
        self.released.append(button)
        self.down.remove(button)

class Input(Singleton):
    def __init__(self):
        self.quit = False
        self.keys = Keys()
        self.mouse = Mouse()
    
    def update(self):
        # Make sure keyboard and mouse data is up-to-date.
        pg.event.pump()
        
        # Make sure the Mouse object resets per-frame info.
        self.mouse.update()
        
        # Loop through events, changing data as necessary.
        for evt in pg.event.get():
            if evt.type == KEYDOWN:
                self.keys.keydown(evt.key)
            elif evt.type == KEYUP:
                self.keys.keyup(evt.key)
            elif evt.type == QUIT:
                self.quit = True
            elif evt.type == MOUSEBUTTONDOWN:
                self.mouse.mouse_down(evt.button)
            elif evt.type == MOUSEBUTTONUP:
                self.mouse.mouse_up(evt.button)
            elif evt.type == MOUSEMOTION:
                self.mouse.mouse_moved(evt.pos, evt.rel)
        
        # Handle globally defined input also.
        if K_ESCAPE in self.keys.pressed:
            self.quit = True