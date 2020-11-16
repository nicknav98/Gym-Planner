from pymorphous.core import *

class IntHood(Device):
    """
    calculate the number of neighbors of the current device, 
    and display it as a red LED
    """
    def step(self):
        self.red = self.sum_hood(self.nbr(1))

spawn_cloud(klass=IntHood)