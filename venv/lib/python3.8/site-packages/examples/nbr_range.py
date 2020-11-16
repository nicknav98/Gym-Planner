from pymorphous.core import *
import random

class NbrRange(Device):
    def step(self):
        self.blue = self.sum_hood(self.nbr_range)*100
        
spawn_cloud(klass=NbrRange)