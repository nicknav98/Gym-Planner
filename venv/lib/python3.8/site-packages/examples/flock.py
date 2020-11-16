from pymorphous.core import *
import random
import numpy

class FlockDemo(Device):
    """ 
    Flocking of all devices
    """
    def setup(self):
        self.free = True
        self.sense1 = True
        self.v = numpy.array([0,0,0])
        
    def step(self):
        """
        (def flock-demo (free)
          (let ((g (green (gradient (sense 2)))))
            (mov
             (if (or free (sense 1)) 
               (flock (vmul 0.1 (nav-grad g))) 
               (vmul 0.1 (disperse))))))
        """
        g = self.gradient(self.sense1)
        self.green = g
        if self.free or self.sense0:
            m = self.flock(0.1 * self.nav_grad(g))
        else:
            m = 0.1 * self.disperse
        self.move(m)

    def flock(self, dir):
        """
        (def flock (dir)
          (rep v 
           (tup 0 0 0)
           (let ((d
              (normalize
               (int-hood
                (if (< (nbr-range) 5)
                  (vmul -1 (normalize (nbr-vec)))
                  (if (> (nbr-range) 10)
                (vmul 0.2 (normalize (nbr-vec)))
                (normalize (nbr v))))))))
             (normalize 
              (+ dir (mux (> (vdot d d) 0) d v))))))
        """
        if self.nbr_range < 5:
            # too close
            tmp = -1 * self.normalize(self.nbr_vec)
        elif self.nbr_range < 10:
            # pretty good
            tmp = 0.2 * self.normalize(self.nbr_vec)
        else:
            # go closer
            tmp = self.normalize(self.nbr(self.v))
            
        d = self.normalize(self.int_hood(tmp))
        return self.normalize(dir + mux(d.dot(d) < 0, d, self.v))

#spawn_cloud(klass=FlockDemo)