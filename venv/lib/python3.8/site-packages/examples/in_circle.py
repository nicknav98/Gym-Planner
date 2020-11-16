from pymorphous.core import *
import numpy

class InCircles(Device):
    """
    is the device in a circle?
    
    ;; To see circles drawn in low, medium, and high resolution, run:
    ;;   proto -n 200 -r 20 -l "(+ (blue (in-circle (tup -40 -20) 30)) (green (in-circle (tup 0 0) 20)))"
    ;;   proto -n 1000 -r 15 -l "(+ (blue (in-circle (tup -40 -20) 30)) (green (in-circle (tup 0 0) 20)))"
    ;;   proto -n 5000 -r 5 -l "(+ (blue (in-circle (tup -40 -20) 30)) (green (in-circle (tup 0 0) 20)))"
    """
    def step(self):
        self.blue = self.in_circle(numpy.array([50, 50, 0]), 30)
        self.green = self.in_circle(numpy.array([0,0,0]), 40)
        
    def in_circle(self, origin, radius):
        """
        (def in-circle (o r)
          (let ((dv (- (probe (coord) 1) o)))
            (< (probe (vdot dv dv) 0) (* r r))))
        """
        dv = self.coord - origin
        return numpy.dot(dv, dv) < radius * radius
        
spawn_cloud(klass=InCircles)