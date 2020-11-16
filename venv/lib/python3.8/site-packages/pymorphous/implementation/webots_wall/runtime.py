""" 
!!!!! This is pseudocode for the webots runtime. Untested! !!!!! 

Defines the wall device
exposes an implementation
"""

import time
import sys
import inspect
import webots_mock as controller
import uuid
from pymorphous.implementaton.simulator.runtime import _Field, _NbrKeyError

_USE_SAFE_NBR = False

class _Message(object):
    def __init__(self, id, time, data):
        self.id = id
        self._time = time
        self._data = data
        
class _BaseDevice(controller.Robot):
    def __init__(self, settings, id, *args, **kwargs):
        super(_BaseDevice, self).__init__(self, *args, **kwargs)
        self.settings = settings
        self._id = id
        self._fields = {} # dict of fields
        self._new_fields = {} # dict of fields
        self._data = {} # dict of values
        self._time = time.time()
        self._nbrs = {} # map neighbor to time
        self._root_frame = None
        self._leds = self._Leds(self)
        self._senses = self._Senses(self)

        controller.register_incoming_message(self._receive_message)
        
    
    @property
    def id(self):
        return self._id
    
    class _Leds(object):
        def __init__(self, parent):
            self.parent = parent

        def __setitem__(self, key, value):
            self.parent.getLed(str(key)).set(value)
        def __getitem__(self, key):
            self.parent.getLed(key)

    @property
    def leds(self):
        return self._leds
    
    @leds.setter
    def leds(self, value):
        for i in range(3):
            self._leds[i] = value[i]
    
    class _Senses(object):
        def __init__(self, parent):
            self.parent = parent

        def __setitem__(self, key, value):
            self.parent.getSense(str(key)).set(value)
        def __getitem__(self, key):
            self.parent.getSense(key)

    @property
    def senses(self):
        return self._senses
    
    @senses.setter
    def senses(self, value):
        for i in range(3):
            self._senses[i] = value[i]

    @property
    def radio_range(self):
        return 0
    
    def move(self, velocity):
        self._velocity = velocity
    
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def x(self):
        return self.coord[0]
    
    @x.setter
    def x(self, value):
        self.coord[0] = value

    @property
    def y(self):
        return self.coord[1]
    
    @y.setter
    def y(self, value):
        self.coord[1] = value
        
    @property
    def z(self):
        return self.coord[2]
    
    @z.setter
    def z(self, value):
        self.coord[2] = value
    
    @property
    def coord(self):
        return self._coord
    
    @coord.setter
    def coord(self, new_coord):
        self._coord = new_coord
    
    def nbr(self, value, extra_key=None):
        if _USE_SAFE_NBR:
            key = repr(["%s:%d" % (f[1], f[2]) for f in inspect.stack(context=0)])
        else:
            frame = None
            frames = []
            i = 1
            while (not frame or frame.f_code.co_filename != self._root_frame.f_code.co_filename 
                and frame.f_lineno != self._root_frame.f_lineno):
                frame = sys._getframe(i)
                i += 1
                frames += [frame]
            key = repr(["%s:%d" % (f.f_code.co_filename, f.f_lineno) for f in frames])
        if extra_key:
            return self._nbr("%s%s" % (key, extra_key), value)
        else:
            return self._nbr(key, value)
            
    def _nbr(self, b, value):        
        if hasattr(self._data, b):
            raise _NbrKeyError("Runtime exception in nbr")
        self._data[b] = value
        return getattr(self._fields, b, _Field())
    
    @property
    def nbr_range(self):
        return _Field()
    
    @property
    def nbr_lag(self):
        return _Field()
    
    def deself(self, field):
        return field
    
    @property
    def dt(self):
        return 0.01
        
    def dostep(self, dt):
        if not self._root_frame:
            self._root_frame = sys._getframe(1)
        self._dt = dt
        self.step()
        self._old_dict = self._dict
        self._dict = {}

    
    def _receive_message(self, message):
        #This is within a signal handler, so no interrupts 
        self._nbrs[message.id] = message.time
        for (b, v) in message.data.items():
            if not hasattr(self._new_fields, b):
                self._new_fields[b] = Field()
            self._new_fields[b][message.id] = value

    
    
    def dostep(self):
        if not self._root_frame:
            self._root_frame = sys._getframe(1)
        self.step()
        self._time = time.time()
        for n in self._nbrs:
            controller.send_message(Message(self.id, self._time, self._data))
        self._data = {}
        # time out old nbrs and field values
        for (n, t) in self._nbrs.items():
            if t + TIMEOUT < self._time:
                del self._nbrs[n]
        for (b, f) in self._fields.items():
            for (id, v) in f.items():
                if not hasattr(self._nbrs, id):
                    del f[id]
        for (b,f) in self._fields.items():
            if len(f) == 0:
                del self._fields[b]

        # bring in the new field values
        controller.disable_interrupts()
        for (b,f) in self._new_fields.items():
            if not hasattr(self._fields, b):
                self._fields[b] = f
            else:
                for (id, v) in f.items():
                    self._fields[id] = v
        controller.enable_interrupts()

def _spawn_cloud(settings, klass=None, args=None, **kwargs):
    """ not sure how to implement """
    o = klass(settings, uuid.uuid4())
    if hasattr(o, 'setup'):
        if args:
            o.setup(*args)
        else:
            o.setup()
    while True:
        o.dostep()