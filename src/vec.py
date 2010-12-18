import numpy as np

class vec2(np.ndarray):
    def __new__(cls, data, y=None, type=None):
        if y == None:
            return np.array((data[0], data[1]), dtype=type, copy=False).view(cls)
        else:
            return np.array((data, y), dtype=type, copy=False).view(cls)
    
    def __getattr__(self, name):
        if name == 'x':
            return self[0]
        elif name == 'y':
            return self[1]
        else:
            raise AttributeError()
    
    def __setattr__(self, name, value):
        if name == 'x':
            self[0] = value
        elif name == 'y':
            self[1] = value
        else:
            self.object.__setattr__(name, value)
