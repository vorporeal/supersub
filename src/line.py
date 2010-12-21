#!/usr/bin/env python

from math import fabs

import pygame as pg
from pygame.locals import *

from vec import *
from graphics import *

def value_between(value, range):
    if range[0] < range[1]:
        if range[0] <= value <= range[1]:
            return True
    elif range[1] <= value <= range[0]:
        return True
    
    return False

def get_line_span(line, axis):
    p1 = np.dot(line.p1, axis)
    p2 = np.dot(line.p2, axis)
    
    if p1 < p2:
        return (p1, p2)
    else:
        return (p2, p1)

# c == center; r == radius
def get_rect_span(rect, axis):
    half_size = vec2(rect.size) / 2.0
    c = np.dot(vec2(rect.center), axis)
    xproj = fabs(np.dot(axis, Line.axis_dir.x))
    yproj = fabs(np.dot(axis, Line.axis_dir.y))
    r = np.dot(vec2(xproj, yproj), half_size)
    return (c - r, c + r)

def axis_intersect(rect, line, axis):
    mins, maxs = get_line_span(line, axis)
    minr, maxr = get_rect_span(rect, axis)
    
    if mins > maxr or maxs < minr:
        return False
    else:
        return True

class Line(object):
    """ This class describes a line in the game world. """
    
    default_color = pg.Color("medium blue")
    axis_dir = vec2(vec2(1, 0), vec2(0, 1))
    
    def __init__(self, p1, p2):
        """ Creates a new Line object.
        
            p1, p2: vec2s (or numpy arrays) representing endpoints of the line. """
        
        self.p1 = p1
        self.p2 = p2
        
        self.vec = p2 - p1
        
        if self.vec.x != 0:
            self.slope = self.vec.y / self.vec.x
        else:
            self.slope = None
        
        self.normal = vec2(-1 * self.vec.y, self.vec.x)
        norm = np.linalg.norm(self.normal)
        if norm != 0:
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
    
    # TODO: Optimize.  Definitely too slow.
    # May not need to optimize, as if a quad-tree is added, this won't get called
    # that frequently.
    def colliderect(self, rect):
        dir = self.p2 - self.p1
        
        if not axis_intersect(rect, self, dir):
            return False
        if not axis_intersect(rect, self, vec2(-dir.y, dir.x)):
            return False
        if not axis_intersect(rect, self, Line.axis_dir[0]):
            return False
        if not axis_intersect(rect, self, Line.axis_dir[1]):
            return False
        
        return True
    
    def project_onto(self, vector):
        vector /= np.linalg.norm(vector)
        p1_proj = np.dot(self.p1, vector) * vector
        p2_proj = np.dot(self.p2, vector) * vector
        return Line(p1_proj, p2_proj)
    
    def intersects_line(self, line):
        for i in {0, 1}:    #0 is y-axis, 1 is x-axis
            axis = vec2(i, 1 - i)
            
            self_proj = self.project_onto(axis)
            line_proj = line.project_onto(axis)
            
            self_proj_vals = (self_proj.p1[1 - i], self_proj.p2[1 - i])
            line_proj_vals = (line_proj.p1[1 - i], line_proj.p2[1 - i])
            
            if value_between(self_proj_vals[0], line_proj_vals):
                continue
            if value_between(self_proj_vals[1], line_proj_vals):
                continue
            if value_between(line_proj_vals[0], self_proj_vals):
                continue
            if value_between(line_proj_vals[1], self_proj_vals):
                continue
            
            return False
        
        return True
