from pymorphous.core import *

class BlueNeighborSense1(Device):
    def step(self):
        self.blue = self.sum_hood(self.nbr(self.sense0))
        
spawn_cloud(klass=BlueNeighborSense1)