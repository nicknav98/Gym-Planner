from pymorphous.core import *
import random

class MultiConsensus(Device):
    def setup(self):
        self.vals = [random.random() * 25, random.random() * 25, random.random() * 25]
        
    def step(self):
        for i in range(len(self.vals)):
            self.leds[i] = self.vals[i]
            # must call with extra_key to disambiguate call site
            self.vals[i] = self.consensus(0.01, self.vals[i], extra_key=i)

spawn_cloud(klass=MultiConsensus)