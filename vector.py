import numpy as np

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def copy(self):
        return Vector(self.x, self.y)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except AttributeError:
            return False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f"<{self.x}, {self.y}>"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
