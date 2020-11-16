from pymorphous.core import *

class BlueSense1(Device):
    def step(self):
        self.blue = self.sense0
        
spawn_cloud(klass=BlueSense1)