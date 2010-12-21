#!/usr/bin/env python

from singleton import *

class Manager(Singleton):
    def __init__(self):
        pass
    
    def update(self, time):
        if not hasattr(self, 'objects'):
            self.objects = []
        toremove = []
        for o in self.objects:
            if hasattr(o, 'update'):
                ret = o.update(time)
                if ret == False:
                    toremove.append(o)
        for o in toremove:
            self.objects.remove(o)
    
    def draw(self, offset):
        for o in self.objects:
            if hasattr(o, 'draw'):
                o.draw(offset)
            