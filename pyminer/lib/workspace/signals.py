import os
import sys
sys.path.append(os.path.dirname(__file__))

from .blinker import signal

workspace_data_changed = signal('workspace-data-changed')
workspace_data_created = signal('workspace-data-created')
workspace_data_deleted = signal('workspace-data-deleted')
