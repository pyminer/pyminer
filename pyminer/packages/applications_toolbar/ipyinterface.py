import typing

if typing.TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.getipython import get_ipython

if __name__ == '__main__':
    get_ipython().applications_toolbar_commands = None


    def __register_commands():
        pass
