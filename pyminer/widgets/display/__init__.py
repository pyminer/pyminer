hint = 'However if your program needn\'t this package,this warning is neglectable.'
try:
    from .matplotlib.qt5agg import PMMatplotlibQt5Widget
except ModuleNotFoundError:
    import warnings

    warnings.warn('matplotlib is not installed. ' + hint)
    pass

from .dynamicgraph import *
