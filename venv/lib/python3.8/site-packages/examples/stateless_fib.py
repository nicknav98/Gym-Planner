from pymorphous.core import *

def fib(n):
    if(n <= 1):
        return 1
    else: 
        return fib(n-1)+fib(n-2)

class BlueFib(Device): 
    def setup(self, n):
        self.n = n
        
    def step(self):
        self.blue = fib(self.n)
        
spawn_cloud(klass=BlueFib, args=[5])