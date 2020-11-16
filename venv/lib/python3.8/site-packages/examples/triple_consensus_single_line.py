from pymorphous.core import *
import random

class TripleConsensusSingleLine(Device):
    def setup(self):
        self.vals = [random.random() * 50, random.random() * 50, random.random() * 50]
        
    def step(self):
        self.leds = [self.vals[0], self.vals[1], self.vals[2]]
        # note that we don't call with extra hash
        self.vals = [self.consensus(0.01, self.vals[0]), self.consensus(0.01, self.vals[1]), self.consensus(0.01, self.vals[2])]

spawn_cloud(klass=TripleConsensusSingleLine)