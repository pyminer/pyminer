import os, sys, json, importlib, threading
from extensionlib import *

'''
This file pretends to be the main program of pyminer_new, which implements
the extensions manager. 
'''

class Extension:
    def __init__(self, info):
        self.name = info.get('name')
        self.displayName = info.get('displayName')
        self.version = info.get('version')
        self.description = info.get('description')

        self.menu = None
        self.menu_info = info.get('menu')
        if self.menu_info:
            self.menu_module = self.import_module(self.menu_info.get('module'))

        self.subwindows = []
        self.subwindows_info = info.get('subWindows', [])
        self.subwindows_modules = {}
        for subwindow_info in self.subwindows_info:
            module_name = subwindow_info.get('module')
            self.subwindows_modules[module_name] = self.import_module(module_name)

        entry_info = info.get('entry')
        module = self.import_module(entry_info.get('module'))
        entry_class = getattr(module, entry_info.get('class'))
        self.entry = entry_class(entry_info.get('config'))

        interface_info = info.get('interface')
        if interface_info:
            module = self.import_module(interface_info.get('module'))
            interface_class = getattr(module, interface_info.get('class'))
            self.interface = interface_class()
            self.public_interface = self.wrap_interface(self.interface)()
    
    def import_module(self, module_name):
        module = importlib.import_module(module_name)
        sys.modules.pop(module_name)
        return module

    def dynamic_binding(self):
        self.entry.run = self.life_period(self.entry.run, self)
        self.entry.start_menu = self.start_menu
        self.entry.start_subwindow = self.start_subwindow
        self.entry.get_interface = self.get_interface

    def start_menu(self, config:dict)->Menu:
        if self.menu != None:
            raise Exception('only one menu instance is allowed')
        if self.menu_info == None:
            raise Exception('no menu is declared')
        menu_cls = getattr(self.menu_module, self.menu_info.get('class'))
        updated_config = self.menu_info.get('config', {})
        updated_config.update(config)
        self.menu = menu_cls(updated_config)
        return self.menu

    def start_subwindow(self, subwindow_class:str, config:dict)->SubWindow:
        for subwindow_info in self.subwindows_info:
            module_name = subwindow_info.get('module')
            subwindow_class_name = subwindow_info.get('class')
            if subwindow_class_name==subwindow_class:
                subwindow_cls = getattr(self.subwindows_modules[module_name], subwindow_class_name)
                updated_config = subwindow_info.get('config', {})
                updated_config.update(config)
                subwindow = subwindow_cls(updated_config)
                self.subwindows.append(subwindow)
                return subwindow
        else:
            raise Exception(f'undefined class {subwindow_class}')

    def life_period(self, run, extension):
        def wrapper(*args, **kwargs):
            extension.start()
            states = run(*args, **kwargs)
            extension.end()
            return states
        return wrapper

    def start(self):
        pass

    def end(self):
        pass

    def wrap_interface(self, original_interface):
        class InterfaceWrapper:
            def __getattribute__(self, attribute):
                obj = original_interface.__getattribute__(attribute)
                if callable(obj):
                    return obj
                else:
                    raise AttributeError(f'{attribute} is hidden for safety')
        return InterfaceWrapper

    def get_interface(self):
        return self.interface


class MainForm :
    def __init__(self):
        self.menus = []
        self.subwindows = []
        self.extensions = []
        self.threads = []

    def load_extension(self, extension_package: str):
        package_path = f'pyminer_new/features/extensions/test_demo/extensions/{extension_package}'
        assert os.path.exists(package_path)
        package_json = f'{package_path}/package.json'
        assert os.path.exists(package_json)
        with open(package_json, 'r') as f:
            package_info = json.loads(f.read())
        sys.path.append(package_path)
        extension = Extension(package_info)
        sys.path.remove(package_path)
        # allow main program to update menu and subwindows to GUI after there are created
        extension.start_menu = self.start_menu(extension.start_menu)
        extension.start_subwindow = self.start_subwindow(extension.start_subwindow)
        # allow main program to do something before start the extension and after it ends
        extension.start = self.start_extension(extension)
        extension.end = self.end_extension(extension)
        # allow the extension to search dependencies and obtain their interfaces
        extension.entry.get_dependency_interface = self.get_dependency_interface
        extension.dynamic_binding()
        self.extensions.append(extension)

    def run_extension(self, extension_name:str):
        for extension in self.extensions:
            if extension.name == extension_name:
                class ExtensionThread(threading.Thread):
                    def run(self):
                        extension.entry.run()
                extensionThread = ExtensionThread()
                extensionThread.start()

    def start_extension(self, extension:Extension):
        def wrapper():
            print(f'start extension {extension.name}')
        return wrapper

    def end_extension(self, extension:Extension):
        def wrapper():
            print(f'end extension {extension.name}')
            print(self.menus, self.subwindows)
            self.menus.remove(extension.menu)
            for subwindow in extension.subwindows:
                self.subwindows.remove(subwindow)
            print(self.menus, self.subwindows)
        return wrapper

    def start_menu(self, start_menu):
        def wrapper(config):
            menu = start_menu(config)
            # following operation is to add menu to the main window
            self.menus.append(menu)
            # a test function
            self.flush()
            return menu
        return wrapper

    def start_subwindow(self, start_subwindow):
        def wrapper(subwindow_class, config):
            subwindow = start_subwindow(subwindow_class, config)
            # following operation is to add subwindow to the main window
            self.subwindows.append(subwindow)
            # a test function
            self.flush()
            return subwindow
        return wrapper

    def flush(self):
        '''
        test only
        '''
        for menu in self.menus:
            menu.test()
        for subwindow in self.subwindows:
            subwindow.test()

    def get_dependency_interface(self, extension_name:str)->object:
        for extension in self.extensions:
            if extension.name==extension_name:
                return extension.public_interface
        else:
            try:
                self.load_extension(extension_name)
                self.run_extension(extension_name)
                return self.get_dependency_interface(extension_name)
            except:
                raise Exception(f'{extension_name} is not loaded')


def main():
    mainForm = MainForm()
    mainForm.load_extension("test_extension2")
    # mainForm.load_extension("test_extension")
    mainForm.run_extension("test_extension2")
    mainForm.run_extension("test_extension")

if __name__ == "__main__":
    main()