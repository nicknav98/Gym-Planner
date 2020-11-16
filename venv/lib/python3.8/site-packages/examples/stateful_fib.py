from pymorphous.core import *

def fib(n):
    if(n <= 1):
        return 1
    else: 
        return fib(n-1)+fib(n-2)
        
class BlueStateFib(Device):
    def setup(self):
        self.n = 0
        
    def step(self):
        self.blue = fib(self.n)
        self.n += 1
        
spawn_cloud(desired_fps=10, klass=BlueStateFib)