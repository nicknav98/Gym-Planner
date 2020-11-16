from pymorphous.core import *
import random

class NavGrad(Device):
    """ 
    Display the distance from a few randomly selected devices
    """
    def setup(self):
        self.sense0 = random.random() < 0.01
        self.gradient = self.Gradient(self)
        
    def step(self):
        """
        (def nav-grad (grad-val)
          (let ((vec-sums
             (fold-hood 
              (fun (res grad-v)
                (if (< grad-v grad-val)
                (tup (vadd (1st res) (nbr-vec)) (+ (2nd res) 1))
                res))
              (tup (tup 0 0) 0)
              grad-val)))
            (if (> (elt vec-sums 1) 0)
            (vmul (/ 1 (2nd vec-sums)) (1st vec-sums)) 
            (tup 0 0))))
        
        ;; For an example of using nav-grad, run:
        ;;   proto -n 500 -r 15 -m -l -s 0.02 -sv "(let ((g (gradient (sense 1))) (which (once (< (rnd 0 1) 0.1)))) (if which (blue 1) 0) (green (< g (inf))) (mov (mux which (nav-grad g) (tup 0 0)))"
        ;; About 1/10 of the devices will turn blue.  Click on a device and
        ;; hit 't'.  As the gradient (green) spreads through the network, the
        ;; blue devices will begin moving to that spot.
        """
        self.red = self.sense0
        self.green = self.gradient.value(self.sense0)

#spawn_cloud(klass=NavGrad)