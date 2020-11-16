"""
exposes an implementation
"""

import random
import numpy
import inspect
import sys
from scipy.spatial import KDTree
import operator
import math
import time

_DEBUG_PRINT_MS = False
_USE_SAFE_NBR = False

import pymorphous.constants

class _NbrKeyError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    
class _Field(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    
    def _op(self, other, op):
        ret = _Field()
        if isinstance(other, _Field):
            for k in self.keys():
                if self[k]!=None and other[k]!=None:
                    ret[k] = op(self[k], other[k])
                else:
                    ret[k] = None       
        else:
            for k in self.keys():
                if self[k]!=None:
                    ret[k] = op(self[k], other)
                else:
                    ret[k] = None
        return ret
    
    def _rop(self, other, op):
        ret = _Field()
        if isinstance(other, _Field):
            for k in self.keys():
                if self[k]!=None and other[k]!=None:
                    ret[k] = op(other[k], self[k])
                else:
                    ret[k] = None       
        else:
            for k in self.keys():
                if self[k]!=None:
                    ret[k] = op(other, self[k])
                else:
                    ret[k] = None
        return ret
    
    def _iop(self, other, iop):
        print self, iop, other
        if isinstance(other, _Field):
            for k in self.keys():
                if self[k]!=None and other[k]!=None:
                    iop(self[k], other[k])
                else:
                    self[k] = None
        else:
            for k in self.keys():
                if self[k]!=None:
                    iop(self[k], other)
                else:
                    self[k] = None
        return self
    
    def __add__(self, other):
        return self._op(other, operator.add)
    
    def __sub__(self, other):
        return self._op(other, operator.sub)
    
    def __radd__(self, other):
        return self._rop(other, operator.add)
    
    def __rsub__(self, other):
        return self._op(other, operator.sub)
    
    def __iadd__(self, other):
        return self._iop(other, operator.iadd)
    
    def __isub__(self, other):
        return self._iop(other, operator.isub)
    
    def __div__(self, other):
        return self._op(other, operator.div)
    
    def __mul__(self, other):
        return self._op(other, operator.mul)
    
    def __rdiv__(self, other):
        return self._rop(other, operator.div)
    
    def __rmul__(self, other):
        return self._rop(other, operator.mul)
    
    def __idiv__(self, other):
        return self._iop(other, operator.idiv)
    
    def __imul__(self, other):
        return self._iop(other, operator.imul)
    
    def __le__(self, other):
        return self._op(other, operator.le)
    
    def __ge__(self, other):
        return self._op(other, operator.ge)
    
    def not_none_values(self):
        ret = []
        for v in self.values():
            if v!=None:
                ret += [v]
        return ret

class _BaseDevice(object):
    def __init__(self, coord, id, cloud):
        # coord is a numpy.array
        self._coord = coord
        self._velocity = numpy.array([0,0,0])
        self._id = id
        self.cloud = cloud
        self._leds = [0, 0, 0]
        self._senses = [0, 0, 0]
        self._nbrs = []
        self._dict = {}
        self._old_dict = {}
        self._dt = 0
        self._nbr_range = _Field()
        self._root_frame = None
    
    @property
    def radio_range(self):
        return self.cloud.radio_range
    
    @property
    def id(self):
        return self._id
    
    @property
    def leds(self):
        return self._leds
    
    @leds.setter
    def leds(self, value):
        self._leds = value
        
    @property
    def senses(self):
        return self._senses
    
    @senses.setter
    def senses(self, value):
        self._senses = value

    def move(self, velocity):
        self._velocity = velocity
    
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def x(self):
        return self._coord[0]
    
    @x.setter
    def x(self, value):
        self.cloud.coord_changed = True
        self._coord[0] = value

    @property
    def y(self):
        return self._coord[1]
    
    @y.setter
    def y(self, value):
        self.cloud.coord_changed = True
        self._coord[1] = value
        
    @property
    def z(self):
        return self._coord[2]
    
    @z.setter
    def z(self, value):
        self.cloud.coord_changed = True
        self._coord[2] = value  
    
    @property
    def coord(self):
        return self._coord
    
    @coord.setter
    def coord(self, new_coord):
        self.cloud.coord_changed = True
        self._coord = new_coord
    
    def getkey(self, extra_key=None):
        if _USE_SAFE_NBR:
            key = repr(["%s:%d" % (f[1], f[2]) for f in inspect.stack(context=0)])
        else:
            frame = None
            frames = []
            i = 2
            while not frame or (frame.f_code.co_filename != self._root_frame.f_code.co_filename 
                and frame.f_lineno != self._root_frame.f_lineno):
                frame = sys._getframe(i)
                i += 1
                frames += [frame]
            key = repr(["%s:%d" % (f.f_code.co_filename, f.f_lineno) for f in frames])
        if extra_key:
            return "%s%s" % (key, extra_key)
        else:
            return key
    
    def nbr(self, val, extra_key=None):
        key = self.getkey(extra_key)
        if key in self._dict.keys():
            raise _NbrKeyError("key %s found twice" % key)
        self._dict[key] = val
        ret = _Field()
        for nbr in self._nbrs + [self]:
            try:
                ret[nbr] = nbr._old_dict[key]
            except KeyError:
                ret[nbr] = None
        return ret
    
    @property
    def nbr_range(self):
        return self._nbr_range
    
    @property
    def nbr_lag(self):
        ret = _Field()
        for nbr in self._nbrs + [self]:
            if nbr == self:
                ret[nbr] = 0
            else:
                ret[nbr] = nbr.dt
        return ret
    
    def deself(self, field):
        f = _Field(field.copy())
        del f[self]
        return f
    
    @property
    def dt(self):
        return self._dt
        
    def dostep(self, dt):
        if not self._root_frame:
            self._root_frame = sys._getframe(1)
        self._dt = dt
        self._reset_leds()
        try:
            self.step()
        except _NbrKeyError, e:
            print e
        self._old_dict = self._dict
        self._dict = {}
        if numpy.any(self.velocity):
            self.coord_changed = True
            self.coord += self.velocity
        

class _Cloud(object):
    def __init__(self, settings, 
                 klass=None, args=None, devices=None, **kwargs):
        self.settings = settings
        for (k, v) in settings.runtime.items():
            self.__dict__[k] = v #setattr does not work with new-style classes
        
        for (k,v) in kwargs.items():
            if not hasattr(self, k):
                raise Exception("no argument", k)
            if v != pymorphous.constants.UNSPECIFIED:
                self.__dict__[k] = v
        
        
        assert(klass or devices)
        assert(self.steps_per_frame == int(self.steps_per_frame) and self.steps_per_frame > 0)
        
        if self._3D:
            if len(self.dim)==3:
                self.dim[2] = self.z_dim
            
        if len(self.dim) == 1:
            self.dim = self.dim + SIMULATOR_DEFAULTS.RUNTIME.DIM[1:]
        elif len(self.dim) == 2:
            self.dim = self.dim + SIMULATOR_DEFAULTS.RUNTIME.DIM[2:] if self._3D else [100]
        
        if not devices:
            devices = []
            if self.grid:
                d = 3 if self.dim[2] else 2
                side_len = math.floor(self.init_num_devices**(1.0/d))
            for i in range(self.init_num_devices):
                if self.grid:
                    if self.dim[2]!=0:
                        coord = numpy.array([self.width*math.floor(i/(side_len*side_len)),
                                           self.height*((i/side_len) % side_len),
                                           self.depth*(i % side_len)])/side_len
                        coord -= numpy.array([self.width/2, self.height/2, self.depth/2])
                    else:
                        coord = numpy.array([self.width*math.floor(i/side_len), 
                                           self.height*(i % side_len), 0])/side_len
                        coord -= numpy.array([self.width/2, self.height/2, 0])
                else:
                    coord = numpy.array([(random.random()-0.5)*self.width, 
                                       (random.random()-0.5)*self.height, 
                                       (random.random()-0.5)*self.depth])
                d = klass(coord = coord,
                          id = i,
                          cloud = self)
                devices += [d]
                if hasattr(d, "setup"):
                    if args:
                        d.setup(*args)
                    else:
                        d.setup()
        self.devices = devices
        
        self.body_rad = self.body_rad if self.body_rad else (0.087*(self.width*self.height/len(devices)))**0.5
        self.window_title = self.window_title if self.window_title else klass.__name__
        
        self.coord_changed = True
        self.mss = []

    @property
    def width(self):
        return self.dim[0]
    
    @property
    def height(self):
        return self.dim[1]
    
    @property
    def depth(self):
        return self.dim[2]
    
    @property
    def num_devices(self):
        return len(self.devices)
    
    def update(self, time_passed):
        epsilon = 0.01
        time_passed = time_passed if time_passed!=0 else epsilon
        for i in range(self.steps_per_frame):
            milliseconds = float(time_passed)/self.steps_per_frame
            if _DEBUG_PRINT_MS:
                self.mss += [milliseconds]
                _mss = self.mss[10:]
                if(len(_mss) % 100):
                    print "milliseconds=%s" % _mss[len(_mss)-1]
            if self.coord_changed:
                point_matrix = numpy.array([d.coord for d in self.devices])
                kdtree = KDTree(point_matrix)
                for d in self.devices:
                    d._nbrs = []
                for (i,j) in kdtree.query_pairs(self.radio_range):
                    self.devices[i]._nbrs += [self.devices[j]]
                    self.devices[j]._nbrs += [self.devices[i]]
                for d in self.devices:
                    d._nbr_range = _Field()
                    for n in d._nbrs + [d]:
                        delta = d.coord - n.coord
                        d._nbr_range[n] = numpy.dot(delta, delta)**0.5
            self.coord_changed = False
            for d in self.devices:
                d.dostep(milliseconds)

def _spawn_cloud(settings, *args, **kwargs):
    cloud = _Cloud(settings, *args, **kwargs)
    if cloud.headless or not cloud.use_graphics:
        last_time = time.time()
        while True:
            now = time.time()
            delta = now - last_time
            cloud.update(delta)
            last_time = now
    else:
        cloud.use_graphics(cloud)