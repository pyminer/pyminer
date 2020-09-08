class Menu:  # class Menu (QtSomeMenuClass):
    """
    Do not create instance of this class, implement
    it and call the function `start_menu` in entry
    class to get its instance.
    """

    def __init__(self, config: dict):
        print(config)

    def test(self):
        print('This a test function of menu')


class SubWindow:  # class SubWindow (QtSomeSubWindowClass):
    """
    Do not create instance of this class, implement
    it and call the function `start_subwindow` in
    entry class to get its instance.
    """

    def __init__(self, config: dict):
        print(config)

    def test(self):
        print('This a test function of subwindow')


class Entry:
    def __init__(self, config: dict):
        print(config)

    def run(self):
        pass

    # Do not use following function in `__init__`
    # Instance of menu and subwindows should be
    # created in `run` function
    def start_menu(self, config: dict) -> Menu:
        return Menu(config)

    def start_subWindow(self, subWindow_class: str, config: dict) -> SubWindow:
        return SubWindow(config)

    def get_interface(self) -> object:
        return object()

    def get_dependency_interface(self, extension_name: str) -> object:
        return object()


class DataClient:  # class DataClient(Client):
    """
    This class provides methods for data exchange
    with the data server. Instances of this class
    can be created in entry's `run` function. The
    variables should be a JSON object that contains
    varnames and corresponding values.
    """

    def write(self, variables: dict):
        pass

    def read(self, varname: str) -> object:
        return None

    def lock(self, varname: str):
        pass

    def unlock(self, varname: str):
        pass

    def read_and_write(self, varname: str, write_func):
        self.lock(varname)
        var = self.read(varname)
        var = write_func(var)
        self.write({varname: var})
        self.unlock(varname)
