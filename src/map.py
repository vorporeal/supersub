#!/usr/bin/env python

import pygame as pg
import numpy as np

from vec import *
from graphics import *
from line import *

class Map(object):
    """ Holds data about the lines which make up the map. """
    
    def __init__(self):
        self.size = vec2(800, 800, type=np.uint16)
        
        self.lines = []
        #self.quadtree = Quadtree(pg.Rect((0, 0), self.size))
        self.g = Graphics()
        
        # If you draw a vertical line with x=width, it would be off-screen
        # (off-by-one error), so compensate.
        sizem = self.size - 2
        
        # Add lines for the borders.
        line = None
        #   TOP
        line = Line(vec2(0,0), vec2(sizem.x,0))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   LEFT
        line = Line(vec2(0,0), vec2(0, sizem.y))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   RIGHT
        line = Line(vec2(0, sizem.y), sizem)
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   BOTTOM
        line = Line(vec2(sizem.x, 0), sizem)
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        
        # Draw a box in the center.
        center = self.size / 2
        #   TOP
        line = Line(center + vec2(-30, -30), center + vec2(30, -30))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   LEFT
        line = Line(center + vec2(-30, -30), center + vec2(-30, 30))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   RIGHT
        line = Line(center + vec2(30, -30), center + vec2(30, 30))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   BOTTOM
        line = Line(center + vec2(-30, 30), center + vec2(30, 30))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        
        # DEBUG #
        #for line in self.lines:
        #    self.quadtree.add(line)
    
    def draw(self, rect=None, surface=None):
        if rect == None:
            rect = self.draw_rect
        if surface == None:
            surface = self.g.screen
        offset = -1 * vec2(rect.topleft)
            
        # Very simple simple optimization.  Gives a speed-up of up to 80fps
        # faster than un-optimized version ("if" statement removed) using simple
        # "borders and corners" map.
        surface.lock()
        for line in self.lines:
            if line.colliderect(rect):
                line.draw(surface, offset)
        surface.unlock()
    
    def update(self, player):        
        # Store some useful variables.
        hres = self.g.res / 2
        
        # Calculate the rectangle we want to draw, using the player as the
        # center.
        top_left = player.pos - hres
        bot_right  = player.pos + hres
        
        # Clip these points to the size of the map.
        top_left_clip = np.clip(top_left, vec2(0, 0), self.size)
        bot_right_clip  = np.clip(bot_right, vec2(0, 0), self.size)
        
        # Make sure we "bump" into the edges of the map.
        for i in [0,1]:
            # Make sure the screen isn't wider/taller than the map.
            if self.g.res[i] > self.size[i]:
                # If it is, center the map in that dimension.
                top_left_clip[i] = (self.size[i] - self.g.res[i]) / 2
                bot_right_clip[i] = top_left_clip[i] + self.g.res[i]
                continue
            # Bump into left/top wall?
            if top_left_clip[i] != top_left[i]:
                bot_right_clip[i] = top_left_clip[i] + self.g.res[i]
            # Bump into right/bottom wall?
            if bot_right_clip[i] != bot_right[i]:
                top_left_clip[i] = bot_right_clip[i] - self.g.res[i]
        
        # Set the draw rectangle using the calculated values.
        self.draw_rect = Rect(top_left_clip, bot_right_clip - top_left_clip)

    def test_collision(self, player):
        bb = player.get_bounding_boxes()
        
        for line in self.lines:
            for box in bb:
                if line.colliderect(box):
                    return True
        return False