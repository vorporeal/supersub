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
        # Keep in mind that there are 60 frames in a second (approx), so we up
        # the speed to compensate.
        self.speed *= 60
        
        self.pos = np.zeros(2)
        self.spawn(pos)
        
        self.image = pg.image.load("media/submarine.png").convert()
        self.image.set_colorkey(pg.Color(255, 0, 255))
        self.image_size = np.array(self.image.get_size(), dtype=np.int8)
        self.half_image_size = self.image_size / 2
    
    def spawn(self, pos):
        # Set initial values for the sub.
        self.health = 100
        self.pos[:] = pos # This does an element-wise copy of pos into self.pos.
    
    # amt is a 2-element numpy translation vector (array)
    def move(self, time, amt):
        # Convert to floating point (as speeds/normalization won't be integral).
        amt = np.float32(amt)
        # Calculate the vector norm.
        norm = np.linalg.norm(amt)
        if norm != 0:
            # Normalize if vector is non-zero.
            amt /= np.linalg.norm(amt)
            # Modify the position, taking into account the speed of the sub.
            self.pos += amt * self.speed * time
    
    def draw(self, offset):
        self.g.screen.blit(self.image, self.pos + offset - self.half_image_size)
    
    def get_bounding_boxes(self):
        ''' Get the list of bounding boxes for the Submarine.
        
            Given as a list of pygame.Rect objects.
        '''
        
        off = self.pos - self.half_image_size
        list = []
        # Top
        list.append(Rect(np.array([12, 6]) + off, (8, 8)))
        # Scope
        list.append(Rect(np.array([24, 8]) + off, (4, 6)))
        # Body
        list.append(Rect(np.array([0, 14]) + off, (32, 12)))
        
        return list
