# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the editor and shell components of the eric6 IDE.

The editor component of the eric6 IDE is based on the Qt port
of the Scintilla editor widget. It supports syntax highlighting, code
folding, has an interface to the integrated debugger and can be
configured to the most possible degree.

The shell component is derived from the editor component and is the visible
component of the interactive language shell. It interacts with the debug
client through the debug server.
"""
