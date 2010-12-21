#!/usr/bin/env python

from vec import *
from line import *
from ping import *
from manager import *

import pygame as pg
from pygame.locals import *

class Beam():
    
    speed = 3.0
    
    # Increase speed to take into account multiplication by time elapsed.
    speed *= 60
    
    def __init__(self, map, pos, dir):
        self.map = map
        
        self.initial_pos = vec2(pos)
        self.pos = pos
        self.dir = dir
    
    def update(self, time):
        new_pos = self.pos + (self.dir * Beam.speed * time)
        movement_line = Line(self.pos, new_pos)
        
        for line in self.map.lines:
            if line.intersects_line(movement_line):
                m = Manager()
                m.objects.append(Ping(self.map, self.pos))
                return False
        
        self.pos = new_pos
        return True
    
    def draw(self, offset):
        g = Graphics()
        
        pg.draw.line(g.screen, pg.Color('grey'), self.initial_pos + offset, self.pos + offset, 5)