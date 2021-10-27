import sys
import os
from PySide2.QtCore import QDir


def get_python_version():
    """
    View the current python version
    """
    ver = sys.version.split(' ')[0]
    if sys.version.find('64 bit') > 0:
        ver = 'Python ' + ver + ' 64-bit'
    else:
        ver = 'Python ' + ver + ' 32-bit'
    return ver


def get_python_modules_directory():
    """
    Function to determine the path to Python's modules directory.

    @return path to the Python modules directory (string)
    """
    import distutils.sysconfig
    return distutils.sysconfig.get_python_lib(True)


def get_pysidemodules_directory(version=2):
    """
    Function to determine the path to PySide2 modules directory.

    @return path to the PySide2 modules directory (string)
    """
    import distutils.sysconfig

    PySidePath = os.path.join(distutils.sysconfig.get_python_lib(True), "PySide{}".format(version))
    if os.path.exists(PySidePath):
        return PySidePath

    return ""

def get_pysideplugins_directory(version=2):
    """
    Function to determine the path to PySide2 plugins directory.

    @return path to the PySide2 plugins directory (string)
    """
    import distutils.sysconfig
    dirname = get_pysidemodules_directory()
    PySidePath = os.path.join(dirname, 'plugins', 'platforms') 
    if os.path.exists(PySidePath):
        return PySidePath

    return ""

def get_scripts_path(version=2):
    """
    Module function to get the path of the PySide tools.

    @param version PySide major version
    @type int
    @return path to the PySide tools
    @rtype str
    """

    path = ""

    program = "pyside{0}-rcc".format(version)
    if sys.platform.startswith(("win", "cygwin")):
        program += ".exe"
        dirName = os.path.dirname(sys.executable)
        if os.path.exists(os.path.join(dirName, program)):
            path = dirName
        elif os.path.exists(os.path.join(dirName, "Scripts", program)):
            path = os.path.join(dirName, "Scripts")
    else:
        dirName = os.path.dirname(sys.executable)
        if os.path.exists(os.path.join(dirName, program)):
            path = dirName

    return path


def get_designer_path(version=2):
    """
    Module function to get the path of the Qt binaries.

    @return path of the Qt binaries
    @rtype str
    """

    path = ""

    program = "designer"
    if sys.platform.startswith(("win", "cygwin")):
        program += ".exe"
        import distutils.sysconfig
        dirName= distutils.sysconfig.get_python_lib(True)
        if os.path.exists(os.path.join(dirName,'PySide{}'.format(version),program)):
            path = os.path.join(dirName,'PySide{}'.format(version),program)

    else:
        dirName = os.path.dirname(sys.executable)
        if os.path.exists(os.path.join(dirName, program)):
            path = dirName

    return path

