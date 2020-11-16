from pymorphous.core import *
import random

class GradientDemo(Device):
    """ 
    Display the distance from a few randomly selected devices
    """
    def setup(self):
        self.sense0 = random.random() < 0.01
        
    def step(self):
        self.red = self.sense0
        self.green = self.gradient(self.sense0)

spawn_cloud(klass=GradientDemo)