from pymorphous.core import *
import numpy

class TrackingDemo(Device):
    """
    Tracking demo
    
    ;; proto -dim 2 2 -n 100 -desired-period 0.1 "(swipe (sense 1))" -T -l -led-flat
    """
    def setup(self, timeout, max_slope, min_dx, sense_id):
        self.timeout = timeout
        self.max_slope = max_slope
        self.min_dx = min_dx
        self.sense_id = sense_id
        self.prev_sense = 0
        self._reset()

    def _reset(self):
        self.tracking = False
        self.init_coord = numpy.array([0,0,0])
        self.time = 0
        
    def step(self):
        """
        (def swipe (src)
          (rep (tup tracking init-x init-y time)
           (tup 0 0 0 0)
           (all
            (if tracking
              (blue 1)
              (blue 0))
            (if (rising-edge src)
              (tup 1 (1st (coord)) (2nd (coord)) 0)
              (if tracking
            (if (> time 50)
              (tup 0 0 0 0)
              (let ((dx (- (1st (coord)) init-x))
                (dy (- (2nd (coord)) init-y)))
                (if (or (< dx 0) (> (/ (abs dy) dx) 0.2))
                  (tup 0 0 0 0)
                  (all 
                   (if (> dx 0.5) (green 1) 0)
                   (tup tracking init-x init-y (+ time (dt)))))))
            (tup 0 0 0 0))))))
        """
        self.blue = self.tracking
        delta = self.coord - self.init_coord
        slope = abs(delta[1])/delta[0]
        
        if not self.prev_sense and self.senses[self.sense_id]:
            # init
            self.tracking = True
            self.init_coord = self.coord
            self.time = 0
        elif (self.tracking 
              and self.time <= self.timeout 
              and delta[0] > 0 
              and slope < self.max_slope): 
            if(self.min_dx > 0.5):
                self.green = 1
            self.time += self.dt
        else:
            self._reset()
            
        self.prev_sense = self.senses[self.sense_id]
        
spawn_cloud(klass=TrackingDemo, args=[50, 0.2, 0.5, 1])

