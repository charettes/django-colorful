from django.utils import version

__all__ = ['VERSION', '__version__']

VERSION = (1, 4, 0, 'final', 0)

__version__ = version.get_version(VERSION)
