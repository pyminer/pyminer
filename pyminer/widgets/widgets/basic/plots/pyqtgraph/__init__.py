import warnings

try:
    import pyqtgraph
    from .base import *
except Exception as e:
    warnings.warn(str(e))
