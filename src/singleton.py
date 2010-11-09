#!/usr/bin/env python

class Singleton(object):
  __single = None # the one, true Singleton

  def __new__(classtype, *args, **kwargs):
    # Check to see if a __single exists already for this class
    # Compare class types instead of just looking for None so
    # that subclasses will create their own __single objects
    if classtype != type(classtype.__single):
      classtype.__single = object.__new__(classtype, *args, **kwargs)
    return classtype.__single

  def __init__(self,name=None):
    self.name = name