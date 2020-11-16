import os
from extensions.registry import stream_registered

try:
    from setuptools.command.egg_info import egg_info as _egg_info
    HAS_SETUPTOOLS = True
except ImportError:
    HAS_SETUPTOOLS = False
    _egg_info = object

class egg_info(_egg_info):

    def run(self):
        if not HAS_SETUPTOOLS:
            # not using egg_info at all
            return
        _egg_info.run(self) # runs setuptools' egg_info

        # adding our extra file
        plugins = stream_registered()
        if plugins != '':
            plugin_file = os.path.join(self.egg_info, 'PLUGINS')
            f = open(plugin_file, 'w')
            try:
                f.write(plugins)
            finally:
                f.close()

