import os

import pymorphous.constants
import pymorphous.implementation.simulator.constants


class _Runtime(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        
        self['init_num_devices'] = 1000
        self['steps_per_frame'] = 1
        self['desired_fps'] = 50
        self['dim'] = [132,100,0]
        self['z_dim'] = 40
        self['body_rad'] = None
        self['radio_range'] = 15
        self['window_width'] = 1024
        self['window_height'] = 768
        self['window_title'] = None
        self['_3D'] = False
        self['headless'] = False
        self['show_leds'] = True
        self['led_flat'] = False
        self['led_stacking_mode'] = pymorphous.implementation.simulator.constants.LED_STACKING_MODE_DIRECT
        self['led_blend'] = False
        self['show_body'] = True
        self['show_radio'] = False
        self['grid'] = False
        self['use_graphics'] = pymorphous.constants.UNSPECIFIED
        
        self['auto_record'] = False
        self['dir_image'] = os.path.join('output', 'image')
        self['tmp_dir_video'] = os.path.join('output', 'video')
        
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value

runtime = _Runtime()

class _Graphics(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        
        self['background_color'] = (0, 0, 0, 0)
        self['simple_body_color'] = (1, 0.25, 0, 0.8)
        self['selected_device_color'] = (1,1,1,0.2)
        self['radio_range_ring_color'] = (0.25, 0.25, 0.25, 0.8)
        self['user_sensor_0_color'] = (1, 0.5, 0, 0.8)
        self['user_sensor_1_color'] = (0.5, 0, 1, 0.8)
        self['user_sensor_2_color'] = (1, 0, 0.5, 0.8)
        self['red_led_color'] = (1, 0, 0, 0.8)
        self['green_led_color'] = (0, 1, 0, 0.8)
        self['blue_led_color'] = (0, 0, 1, 0.8)
        
        self['simple_body_dim'] = (0.8, 2, 2)
        self['select_dim'] = (0.8*4, 8, 8)
        self['selected_device_dim'] = (0.8*4, 8, 8)
        self['user_sensor_0_dim'] = (0.8, 8, 8)
        self['user_sensor_1_dim'] = (0.8, 8, 8)
        self['user_sensor_2_dim'] = (0.8, 8, 8)
        self['red_led_dim'] = (0.4, 8, 8)
        self['green_led_dim'] = (0.4, 8, 8)
        self['blue_led_dim'] = (0.4, 8, 8)
    
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value
    
    @property
    def _user_sensor_colors(self):
        return [self.user_sensor_0_color, self.user_sensor_1_color, self.user_sensor_2_color]
    
    @property
    def _led_colors(self):
        return [self.red_led_color, self.green_led_color, self.blue_led_color]
    
    @property
    def _user_sensor_dims(self):
        return [self.user_sensor_0_dim, self.user_sensor_1_dim, self.user_sensor_2_dim]
    
    @property
    def _led_dims(self):
        return [self.red_led_dim, self.green_led_dim, self.blue_led_dim]

graphics = _Graphics()

target_runtime = 'simulator'