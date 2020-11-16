from pymorphous.core import *
import random

class Consensus(Device):
    def setup(self):
        self.val = random.random() * 10
        
    def step(self):
        self.red = self.val
        # note that we don't call with extra hash
        self.val = self.consensus(0.01, self.val)
        
spawn_cloud(klass=Consensus)