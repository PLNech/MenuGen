import os
import sys

__author__ = 'PLNech'


def cpu_count():
    """
    Returns the number of CPUs in the system
    """
    num = 0
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            pass
    elif sys.platform == 'darwin':
        try:
            num = int(os.popen('sysctl -n hw.ncpu').read())
        except ValueError:
            pass
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            pass

    if num >= 1:
        return num
    else:
        raise NotImplementedError
