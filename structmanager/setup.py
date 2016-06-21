from __future__ import division, print_function, absolute_import

import os
from distutils.sysconfig import get_python_lib
from subprocess import Popen
import shutil


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('structmanager', parent_package, top_path)

    config.add_subpackage('analysis')
    config.add_subpackage('excel')
    config.add_subpackage('methods')
    config.add_subpackage('optimization')
    config.add_subpackage('outreader')
    config.add_subpackage('structelem')

    config.make_config_py()

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
