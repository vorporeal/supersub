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
        
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, surface, offset):
        """ Draws the line to the screen. """
        
        g = Graphics()
        
        # Determine the color of the line.
        color = None
        if hasattr(self, "color"):
            color = self.color
        else:
            color = Line.default_color
            
        pg.draw.line(surface, color, np.int32(self.p1 + offset), np.int32(self.p2 + offset), 2)
