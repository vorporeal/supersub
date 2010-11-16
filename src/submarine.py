#!/usr/bin/env python

from graphics import *
import numpy as np
import pygame as pg
from pygame.locals import *

class Sub(object):
    # pos is a 2-element object storing the position of the sub as a vector.
    def __init__(self, pos):
        self.g = Graphics()
        #self.speed = np.array([0.5, 0.3])
        self.speed = np.array([2.0, 1.2]) # To assist with testing.
        self.spawn(pos)
    
    def spawn(self, pos):
        # Set initial values for the sub.
        self.health = 100
        
        self.pos = np.array(pos)
    
    # amt is a 2-element numpy translation vector (array)
    def move(self, amt):
        # Convert to floating point (as speeds/normalization won't be integral).
        amt = np.float32(amt)
        # Calculate the vector norm.
        norm = np.linalg.norm(amt)
        if norm != 0:
            # Normalize if vector is non-zero.
            amt /= np.linalg.norm(amt)
            # Modify the position, taking into account the speed of the sub.
            self.pos += amt * self.speed
    
    def draw(self, offset):
        pg.draw.circle(self.g.screen, pg.Color("cornflower blue"), np.int32(self.pos + offset), 12)
