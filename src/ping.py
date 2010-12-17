import pygame as pg
from pygame.locals import *

from vec import *
from graphics import *

class Ping():
    ''' A class to handle the visible pings due to use of active sonar. '''
    
    # The number of seconds a ping should take to fade out completely.
    fade_time = 3.0
    
    # The size info for the ping.
    side_len = 50
    side_len_arr = vec2(side_len, side_len)
    radius = side_len / 2
    radius_arr = vec2(radius, radius)
    
    def __init__(self, map, pos):
        self.time = 0.0
        self.pos = vec2(pos)
        self.g = Graphics()
        self.alpha = 0xFF
        self.__render(map)
    
    def __render(self, map):
        # Create a new surface which will store the "picture" of this ping.
        self.image = pg.Surface(Ping.side_len_arr, 0, self.g.screen)
        
        # Draw the ping to the surface.
        map.draw(pg.Rect(self.pos - Ping.radius_arr,
                         self.pos + Ping.radius_arr), self.image)
        
        # Make sure it has per-pixel alpha for the mask to work properly.
        self.image.convert_alpha()
        # TODO: Blit a "falloff mask" on top of the visible lines.
        
        # Convert back to using surface-wide alpha.
        self.image.convert()
        # Make the image opaque.
        self.image.set_alpha(0xFF)
    
    def update(self, time):
        # Modify the alpha by the elapsed time.
        self.alpha -= 0xFF * (time / Ping.fade_time)
        # Clamp the bottom end to zero.
        if int(self.alpha) <= 0.0:
            self.alpha = 0.0
        # Set the surface's alpha.
        self.image.set_alpha(int(self.alpha))
    
    def draw(self, offset):
        # If we draw the map, you won't see pings!!!
        self.g.screen.blit(self.image, self.pos - Ping.radius_arr + offset)