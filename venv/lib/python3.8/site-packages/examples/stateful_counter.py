from pymorphous.core import *

class BlueCounter(Device):
    def setup(self):
        self.c = 0
        
    def step(self):
        self.blue = self.c
        self.c += 1

spawn_cloud(klass=BlueCounter)    