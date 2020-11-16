from pymorphous.core import *
import random

class DualConsensus(Device):
    def setup(self):
        self.vals = [random.random() * 50, random.random() * 50]
        
    def step(self):
        self.red = self.vals[0]
        # note that we don't call with extra hash
        self.vals[0] = self.consensus(0.01, self.vals[0])
        self.green = self.vals[1]
        self.vals[1] = self.consensus(0.01, self.vals[1])

spawn_cloud(klass=DualConsensus)