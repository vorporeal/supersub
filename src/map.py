#!/usr/bin/env python

from math import *

import pygame as pg
import numpy as np

from graphics import *
from line import *

axis_dir = [np.array([1, 0]), np.array([0, 1])]

def get_line_span(line, axis):
    p1 = np.dot(line.p1, axis)
    p2 = np.dot(line.p2, axis)
    
    # Return the min and max span as (min, max).
    if p1 < p2:
        return (p1, p2)
    else:
        return (p2, p1)

# c == center; r == radius
def get_rect_span(rect, axis):
    half_size = np.array(rect.size) / 2.0
    c = np.dot(np.array(rect.center), axis)
    xproj = fabs(np.dot(axis, axis_dir[0]))
    yproj = fabs(np.dot(axis, axis_dir[1]))
    r = np.dot(np.array((xproj, yproj)), half_size)
    return (c - r, c + r)

def axis_intersect(rect, line, axis):
    mins, maxs = get_line_span(line, axis)
    minr, maxr = get_rect_span(rect, axis)
    
    if mins > maxr or maxs < minr:
        return False
    else:
        return True

# TODO: Optimize.  Definitely too slow.
def line_rect_collision(line, rect):
    dir = line.p2 - line.p1
    
    if not axis_intersect(rect, line, dir):
        return False
    if not axis_intersect(rect, line, np.array((-dir[0], dir[1]))):
        return False
    if not axis_intersect(rect, line, axis_dir[0]):
        return False
    if not axis_intersect(rect, line, axis_dir[1]):
        return False
    
    return True

class Map(object):
    """ Holds data about the lines which make up the map. """
    
    def __init__(self):
        self.lines = []
        self.g = Graphics()
        
        self.size = np.array([800, 800], dtype=np.uint16)
        
        # If you draw a vertical line with x=width, it would be off-screen
        # (off-by-one error), so compensate.
        sizem = self.size - 2
        
        # Add lines for the borders.
        line = None
        #   TOP
        line = Line(np.array([0,0]), np.array([sizem[0],0]))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   LEFT
        line = Line(np.array([0,0]), np.array([0, sizem[1]]))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   RIGHT
        line = Line(np.array([0, sizem[1]]), sizem)
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   BOTTOM
        line = Line(np.array([sizem[0], 0]), sizem)
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        
        # Draw a box in the center.
        center = self.size / 2
        #   TOP
        line = Line(center + np.array([-30, -30]), center + np.array([30, -30]))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   LEFT
        line = Line(center + np.array([-30, -30]), center + np.array([-30, 30]))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   RIGHT
        line = Line(center + np.array([30, -30]), center + np.array([30, 30]))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
        #   BOTTOM
        line = Line(center + np.array([-30, 30]), center + np.array([30, 30]))
        line.color = pg.Color("dark blue")
        self.lines.append(line)
    
    def draw(self, rect=None, surface=None):
        if rect == None:
            rect = self.draw_rect
        if surface == None:
            surface = self.g.screen
        offset = -1 * np.array(rect.topleft)
            
        # Very simple simple optimization.  Gives a speed-up of up to 80fps
        # faster than un-optimized version ("if" statement removed) using simple
        # "borders and corners" map.
        surface.lock()
        for line in self.lines:
            if line_rect_collision(line, rect):
                line.draw(offset)
        surface.unlock()
    
    def update(self, player):
        # Make sure the map's not smaller than the window.
        # NOTE: THIS IS INCORRECT.  It shouldn't correctly handle maps that are
        #       smaller than the window in only one dimension.
        if np.all(self.size < self.g.res):
            return Rect(self.size - self.g.res, self.g.res)
        
        # Store some useful variables.
        hres = self.g.res / 2
        
        # Calculate the rectangle we want to draw, using the player as the
        # center.
        top_left = player.pos - hres
        bot_right  = player.pos + hres
        
        # Clip these points to the size of the map.
        top_left_clip = np.clip(top_left, np.zeros(2), self.size)
        bot_right_clip  = np.clip(bot_right, np.zeros(2), self.size)
        
        # Make sure we "bump" into the edges of the map.
        for i in [0,1]:
            #   Bump into left/top wall?
            if top_left_clip[i] != top_left[i]:
                bot_right_clip[i] = top_left_clip[i] + self.g.res[i]
            #   Bump into right/bottom wall?
            if bot_right_clip[i] != bot_right[i]:
                top_left_clip[i] = bot_right_clip[i] - self.g.res[i]
        
        # Set the draw rectangle using the calculated values.
        self.draw_rect = Rect(top_left_clip, bot_right_clip - top_left_clip)

    def test_collision(self, player):
        bb = player.get_bounding_boxes()
        
        for line in self.lines:
            for box in bb:
                if line_rect_collision(line, box):
                    return True
        return False