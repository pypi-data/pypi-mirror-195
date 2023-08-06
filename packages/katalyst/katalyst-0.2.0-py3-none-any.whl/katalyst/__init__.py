import sys

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

__version__ = metadata.version(__package__ or __name__)
__version_info__ = tuple(map(int, __version__.split('.')))
