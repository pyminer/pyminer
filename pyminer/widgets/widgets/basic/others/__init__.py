import typing
from .gauge import *
from .processconsole import PMGProcessConsoleWidget
from .instantbootconsole import PMGInstantBootConsoleWidget
if typing.TYPE_CHECKING:
    import widgets.widgets.basic.others.console as console


def import_console_class() -> typing.Type['console.PMGIpythonConsole']:
    """
    导入这一步是耗时操作。为了节约widgets导入的时间，就使用了这种方式动态导入类。
    Returns:

    """
    import widgets.widgets.basic.others.console as console
    return console.PMGIpythonConsole
