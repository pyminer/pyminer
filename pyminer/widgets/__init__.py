import time

t0 = time.time()
import logging

logger = logging.getLogger('widgets_init')

pmgprint = lambda *x: print(*x)
from .elements import *
from .utilities import *
from .widgets import *
from .flowchart import *
from .get_time_consuming_classes import get_ipython_console_class

t1 = time.time()
logger.warning('widgets loading time: %f s' % (t1 - t0))

