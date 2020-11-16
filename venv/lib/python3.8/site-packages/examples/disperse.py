"""
Test dispersion
"""
from pymorphous.core import *

class Disperse(Device):
    def step(self):
        self.move(0.1 * self.disperse)

spawn_cloud(klass=Disperse)