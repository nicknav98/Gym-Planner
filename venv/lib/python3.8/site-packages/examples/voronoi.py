"""
Voronoi by Andrew Kessel
https://github.com/amkessel/AMK-proto-examples/blob/master/voronoi-decomposition-simple.proto
"""
from pymorphous.core import *
import random

class Voronoi(Device):
    def step(self):
        self.dists = {}
        for i in range(3):
            self.dists[i] = self.gradient(self.senses[i], extra_key=i)
        self.closest = min(self.dists,key = lambda a: self.dists.get(a))
        if self.dists[self.closest] < 50: #max_distance
            self.leds[self.closest] = 5

spawn_cloud(klass=Voronoi)