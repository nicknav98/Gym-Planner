"""
Demonstrates extensions
"""

from pymorphous.core import *
import random
from extensions.contrail_graphics import contrail_graphics

class Move(Device):
    def step(self):
        self.move([(random.random()-0.5)*2, (random.random()-0.5)*2, 0])
        
spawn_cloud(klass=Move)#, use_graphics=contrail_graphics)
