#!/usr/bin/env python

import pygame as pg

from graphics import *
from line import *

def line_rect_collision(line, rect):
    """ Does a collision test between a Line and a pygame.Rect. """
    
    xmin, ymin = rect.topleft
    xmax, ymax = rect.bottomright
    
    '''
    if (line.p2[0] - line.p1[0]) == 0:
        if line.p1[1] <= ymin and line.p2[1] >= ymin:
            return True
        elif line.p1[1] > ymin and line.p2[1] <= ymin:
            return True
        elif line.p2[1] <= ymin and line.p1[1] >= ymin:
            return True
        elif line.p2[1] > ymin and line.p1[1] <= ymin:
            return True
        else:
            return False
    
    m = (line.p2[1] - line.p1[1]) / (line.p2[0] - line.p1[0])
    b = line.p1[1] - m * line.p1[0]
    
    for point in [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]:
        y = m * point[0] + b
        if y >= ymin and y <= ymax:
            return True
    return False'''
    
    '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
    
    # Assume the line is vertical.
    m = None
    b = line.p1[0]
    # If not, calculate its slope (we're avoiding div-by-zero).
    if not line.p2[0] == line.p1[0]:    
        m = (line.p2[1] - line.p1[1]) / (line.p2[0] - line.p1[0])
    if not m == None:
        b = line.p1[1] - m * line.p1[0]
    
    # We'll test intersection with the box by testing the locations of
    # its intersections with the four lines comprising the rect.
    
    for point in [rect.topleft, rect.bottomright]:
        # Do a special test for vertical lines (as m == inf == None).
        if m == None:
            if xmin <= line.p1[0] <= xmax:
                return True
            else:
                return False
        # Test rect's horizontal lines first.
        y = m * point[0] + b
        if ymin <= y <= ymax:
            return True
        # Do a special test for horizonal lines (to avoid div-by-zero).
        if m == 0:
            if ymin <= line.p1[1] <= ymax:
                return True
            else:
                return False
        # Now test its vertical lines.
        x = (point[1] - b) / m
        if xmin <= x <= xmax:
            return True
    return False

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
    
    def draw(self):
        offset = -1 * np.array(self.draw_rect.topleft)
        self.g.screen.lock()
        for line in self.lines:
            #if self.draw_rect.collidepoint(line.p1) or self.draw_rect.collidepoint(line.p2):
            #if line_rect_collision(line, self.draw_rect):
            line.draw(offset)
        self.g.screen.unlock()
    
    def update(self, player):
        # Make sure the map|s not smaller than the window.
        # NOTE: THIS IS INCORRECT.  It shouldn|t correctly handle maps that are
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