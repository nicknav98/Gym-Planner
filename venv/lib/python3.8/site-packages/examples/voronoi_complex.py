"""
Voronoi by Andrew Kessel
"""
from pymorphous.core import *
import random

class ComplexVoronoi(Device):
    def closest(self, expr):
        """ return the closest device with expr """
        return self
    
    def step(self):
        closest = self.closest(self.sense0)
        if closest:
            self.leds = closest.color

spawn_cloud(klass=ComplexVoronoi, led_blend=True)