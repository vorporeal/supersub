#!/usr/bin/env python

from graphics import *
import numpy as np
import pygame as pg
from pygame.locals import *

class Sub(object):
    # pos is a 2-element numpy array storing the position of the sub
    #   as a vector.
    def __init__(self, pos):
        self.g = Graphics()
        self.speed = np.array([0.5, 0.3])
        self.spawn(pos)
    
    def spawn(self, pos):
        # Set initial values for the sub.
        self.health = 100
        
        self.pos = pos
    
    # amt is a 2-element numpy translation vector (array)
    def move(self, amt):
        # Normalize the movement vector.
        norm = np.linalg.norm(amt)
        if norm != 0:
            amt /= np.linalg.norm(amt)
        # Modify the position, taking into account the speed of the sub.
        self.pos += amt * self.speed
    
    def draw(self):
        pg.draw.circle(self.g.screen, pg.Color("cornflower blue"), self.pos, 12)
