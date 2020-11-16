from pymorphous.core import *
import random

class MinPlusDemo(Device):
    def setup(self):
        self.sense0 = random.random()
        
    def step(self):
        self.red = self.sense0
        self.green = self.min_hood_plus(self.nbr(self.sense0))

spawn_cloud(klass=MinPlusDemo)