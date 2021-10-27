try:
    from .lines import *
except ImportError as e:
    import warnings
    warnings.warn(str(e))