from ...extensionlib import Entry
import time


class YourEntry(Entry):
    def run(self):
        # entry class has access of its menu and subwindows
        # but it has no access of the instance of mainwindow
        menu = self.start_menu({'param': 3})
        subwindow1a = self.start_subwindow('YourSubWindow1', {})
        subwindow1b = self.start_subwindow('YourSubWindow1', {})
        subwindow2 = self.start_subwindow('YourSubWindow2', {})
        interface = self.get_interface()
        interface._link_(self)
        dependency_interface = self.get_dependency_interface('test_extension')
        print('我是插件2')
        time.sleep(2)
        # entry class can obtain public interface of other extension
        dependency_interface.method()
        try:
            print(dependency_interface.entry)
        except AttributeError:
            print(f'{dependency_interface} doesn\'t have access of entry')
