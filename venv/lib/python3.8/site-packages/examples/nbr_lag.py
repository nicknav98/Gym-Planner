from pymorphous.core import *
import random

class NbrLag(Device):
    def step(self):
        self.blue = self.max_hood(self.nbr_lag)
        
spawn_cloud(klass=NbrLag)