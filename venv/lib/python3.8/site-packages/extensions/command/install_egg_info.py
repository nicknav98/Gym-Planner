# -*- coding: utf8 -*-
"""This command will create a directory for egg.info
at installation time, and add two files in it:

    - PKG-INFO: the metadata
    - PLUGINS: plugins
"""
try:
    from setuptools.command.install_egg_info import \
        install_egg_info as _install_egg_info
    HAS_SETUPTOOLS = True
except ImportError:
    from distutils.command.install_egg_info import \
        install_egg_info as _install_egg_info
    HAS_SETUPTOOLS = False

import os, shutil
from distutils import log, dir_util
from extensions.registry import stream_registered

class install_egg_info(_install_egg_info):
    """Install an .egg-info directory for the package"""

    def _ensure_directory(self, path):
        """Ensure that the parent directory of `path` exists"""
        dirname = os.path.dirname(path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def run(self):
        if HAS_SETUPTOOLS:
            # PLUGINS is added by egg_info
            return _install_egg_info.run(self)
        # creating the egg.info file
        target = self.target
        if os.path.isdir(self.target) and not os.path.islink(self.target):
            dir_util.remove_tree(self.target, dry_run=self.dry_run)
        elif os.path.exists(self.target):
            self.execute(os.unlink, (self.target,), "Removing "+self.target)
        if not self.dry_run:
            self._ensure_directory(self.target)

        # creating the target directory
        os.mkdir(self.target)

        # creating the PKG-INFO file
        pkg_info = os.path.join(self.target, 'PKG-INFO')
        f = open(pkg_info, 'w')
        try:
            self.distribution.metadata.write_pkg_file(f)
        finally:
            f.close()

        self._add_plugins()

    def _add_plugins(self):
        # creating PLUGINS
        plugins = stream_registered()
        if plugins != '':
            plugin_file = os.path.join(self.target, 'PLUGINS')
            f = open(plugin_file, 'w')
            try:
                f.write(plugins)
            finally:
                f.close()

