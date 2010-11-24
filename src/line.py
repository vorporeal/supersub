#!/usr/bin/env python

import pygame as pg
from pygame.locals import *

from graphics import *

class Line(object):
    """ This class describes a line in the game world. """
    
    default_color = pg.Color("medium blue")
    
    def __init__(self, p1, p2):
        """ Creates a new Line object.
        
            p1, p2: numpy arrays representing endpoints of the line. """
        
        if np.all(p1 == p2):
            raise Exception("can't create a line with length 0!")
        
        self.p1 = p1
        self.p2 = p2
        
        self.vec = p2 - p1
        
        if self.vec[0] != 0:
            self.slope = self.vec[1] / self.vec[0]
        else:
            self.slope = None
        
        self.normal = np.array((-1 * self.vec[1], self.vec[0]))
        self.normal /= np.linalg.norm(self.normal)
    
    def draw(self, surface, offset):
        """ Draws the line to the screen. """
        
        g = Graphics()
        
        # Determine the color of the line.
        color = None
        if hasattr(self, "color"):
            color = self.color
        else:
            color = Line.default_color
        
        p1 = np.int32(self.p1 + offset)
        p2 = np.int32(self.p2 + offset)
        
        pg.draw.line(surface, color, p1, p2, 2)
    
    def reflect(self, incident):
        """ Reflects a vector off of this line. """
        
        return incident - 2 * np.dot(self.normal, incident) * self.normal
