# -*- coding: utf8 -*-
""" This module makes sure install_egg_info is triggered.
"""

# until distutils is pluggable, this is
# the less intrusive way to register this install_egg_info command
import sys
from distutils.dist import Distribution
from extensions.command.install_egg_info import install_egg_info
from extensions.command.egg_info import egg_info

CMD_MODULE = 'extensions.command'

def get_command_class(self, command):
    """Pluggable version of get_command_class()"""
    if (self.command_packages is not None and
        CMD_MODULE not in self.command_packages):
        self.command_packages.append(CMD_MODULE)
    self.cmdclass['install_egg_info'] = install_egg_info
    self.cmdclass['egg_info'] = egg_info
    return self._old_get_command_class(command)

Distribution._old_get_command_class = Distribution.get_command_class
Distribution.get_command_class = get_command_class

