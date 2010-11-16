#!/usr/bin/env python

import pygame as pg
from pygame.locals import *

import numpy as np

from graphics import *
from submarine import *
from input import *
from map import *
from line import *

def start():
    # Initialize pygame
    pg.init()
    
    # Create our graphics manager.
    g = Graphics()
    g.set_res((640, 480))
    
    # Create our input handler.
    i = Input()
    
    # Create a sub.
    sub = Sub(np.array([320, 240], dtype=np.float32))
    
    # Create a Clock with which to synchronize updates.
    clock = pg.time.Clock()
    
    # A small counter to limit how frequently we update the fps text.
    fps_counter = 0
    # A surface to store the fps text on.
    fps_text = None
    
    # Create a font with which to blit text to the screen.
    font = pg.font.Font(pg.font.match_font('dejavusans'), 12)
    
    # Create a map, and add a line to it.
    map = Map()
    map.lines.append(Line(np.array([50, 0]), np.array([0, 50])))
    map.lines.append(Line(np.array([750, 800]), np.array([800, 750])))
    
    # A simple event loop.
    while not i.quit:
        # Make sure the input data is up-to-date.
        i.update()
        
        move_vec = np.array([0,0], dtype=np.float32)
        
        if K_w in i.keys.pressed:
            move_vec += np.array([0,-1])
        if K_a in i.keys.pressed:
            move_vec += np.array([-1,0])
        if K_s in i.keys.pressed:
            move_vec += np.array([0,1])
        if K_d in i.keys.pressed:
            move_vec += np.array([1,0])
        
        # Move the submarine based on the input.
        sub.move(move_vec)
        
        # Update the map with the new player position.
        map.update(sub)
        
        # Clear the screen.
        g.clear()
        
        # Draw the map.
        map.draw()
        
        # Calculate the sub's offset, and draw it.
        sub_offset = -1 * np.array(map.draw_rect.topleft)
        sub.draw(sub_offset)
        
        # Update fps_text if it's been 12 ticks since the last update.
        if fps_counter == 0:
            fps_text = font.render(str(clock.get_fps()), True, pg.Color("light grey"))
        # Blit fps_text to the screen.
        g.screen.blit(fps_text, (0,0))
        
        # Increment and mod the fps_counter.
        fps_counter = (fps_counter + 1) % 12
        
        # Update the screen.
        g.flip()
        
        # Wait till "v-sync" - limit the framerate to 60, more or less.
        clock.tick(60)