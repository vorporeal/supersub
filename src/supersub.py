#!/usr/bin/env python

import pygame as pg
from pygame.locals import *

import numpy as np

from vec import *
from graphics import *
from submarine import *
from input import *
from map import *
from line import *
#from ping import *

WIDTH = 840
HEIGHT = 840

def start():
    # Initialize pygame
    pg.init()
    
    # Create our graphics manager.
    g = Graphics()
    g.set_res((WIDTH, HEIGHT))
    
    # Set the caption for the display
    pg.display.set_caption('Super Sub')
    
    # Create our input handler.
    i = Input()
    
    # Create a sub.
    sub = Sub(vec2(320, 240, type=np.float32))
    
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
    map.lines.append(Line(vec2(50, 0), vec2(0, 50)))
    map.lines.append(Line(vec2(750, 800), vec2(800, 750)))
    
    # Define a variable to store the frame times.
    time = 0
    
    # Define a list to store Ping objects.
    pings = []
    
    # A simple event loop.
    while not i.quit:
        # Make sure the input data is up-to-date.
        i.update()
        
        # Get the elapsed time (for calculating movement properly).
        time = clock.get_time() / 1000.0
        
        # Update all pings.
        #for p in pings:
        #    p.update(time)
        
        # Create a new Ping if the mouse was clicked.
        #if 1 in i.mouse.clicked:
        #    pings.append(Ping(map, i.mouse.pos + vec2(map.draw_rect.topleft)))
        
        # Create a zero-vector to store the movement direction for the sub.
        dir = vec2(0.0, 0.0, type=np.float32)
        
        # Calculate the direction vector based on user input.
        if K_w in i.keys.pressed:
            dir += vec2(0.0, -1.0)
        if K_a in i.keys.pressed:
            dir += vec2(-1.0, 0.0)
        if K_s in i.keys.pressed:
            dir += vec2(0.0, 1.0)
        if K_d in i.keys.pressed:
            dir += vec2(1.0, 0.0)
        
        # Move the submarine.
        move_vec = sub.move(time, dir)
        # If the move is invalid, respawn the dead submarine (for now).
        # TODO: "Kill" the sub, and handle the death (end of match, give a point
        #       and respawn?).        
        if map.test_collision(sub):
            sub.spawn(vec2(320, 240))
        
        # Update the map with the new player position.
        map.update(sub)
        
        # Clear the screen.
        g.clear()
        
        # Draw the map.
        map.draw()
        
        # Calculate the drawing offset.
        offset = -1 * vec2(map.draw_rect.topleft)
        
        # Draw any pings.
        #for p in pings:
        #    if p.alpha == 0:
        #        pings.remove(p)
        #    else:
        #        p.draw(offset)
        
        # Draw the sub.
        sub.draw(offset)
        
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
        clock.tick()
