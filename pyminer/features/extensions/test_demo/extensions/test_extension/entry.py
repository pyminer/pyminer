from extensionlib import Entry
import time

class MyEntry(Entry):
    def run(self):
        # entry class has access of its menu and subwindows
        # but it has no access of the instance of mainwindow
        menu = self.start_menu({'param':3})
        subwindow1a = self.start_subwindow('MySubWindow1', {})
        subwindow1b = self.start_subwindow('MySubWindow1', {})
        subwindow2 = self.start_subwindow('MySubWindow2', {})
        interface = self.get_interface()
        interface._link_(self)
        
        time.sleep(1)