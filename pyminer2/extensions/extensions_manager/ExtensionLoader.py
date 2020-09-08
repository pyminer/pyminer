import os
import sys
import importlib
import json
from collections import namedtuple
import copy
import traceback

from pyminer2.extensions.extensions_manager import log
from pyminer2.pmutil import get_root_dir

BASEDIR = get_root_dir()

Info = namedtuple('Info',
                  ['icon',
                   'name',
                   'display_name',
                   'version',
                   'description',
                   'path'])


class PublicInterface:
    pass


class ExtensionLoader:
    def __init__(self):
        # 这里不能直接写self.path,因为所有入口文件都叫main.py,会被Python缓存起来
        self.import_path = os.path.join(BASEDIR, 'extensions','packages')
        sys.path.append(self.import_path)  # 将模块导入路径设置为扩展文件夹,这样可以直接导入入口文件
        self.extension_lib_path = os.path.join(BASEDIR, 'extensions','extensionlib')
        sys.path.append(self.extension_lib_path)

    def load(self, file, ui_inserters):
        self.package = json.load(file)
        self.ui_inserters = ui_inserters
        try:
            self.name = self.package['name']
            self.display_name = self.package['display_name']
            self.version = self.package['version']
            self.description = self.package['description']
            self.icon = self.package['icon']

            self.path = os.path.join(
                BASEDIR,
                'extensions','packages',
                self.name)  # 扩展文件夹路径

            main_config = self.package.get('main', {'file':'main.py', 'main':'Extension'})
            main_class = self.load_class(main_config['file'], main_config['main'])
            self.main = main_class()

            interface_config = self.package.get('interface', {'file':'main.py', 'interface':'Interface'})
            self.main.interface = self.load_class(
                interface_config['file'], interface_config['interface'])()
            self.main.public_interface = self.create_public_interface(
                self.main.interface)

            for key in getattr(self.main.interface, 'ui_inserters', []):
                self.ui_inserters[f'extension_{self.name}_{key}'] = self.main.interface.ui_inserters[key]

            from pyminer2.extensions.extensionlib.extension_lib import extension_lib
            self.main.extension_lib = extension_lib

            self.main.widget_classes = {}
            self.main.widgets = {}  # store auto inserted widgets
            for widget in self.package['widgets']:
                widget_class = self.load_widget(widget)
                widget_class_name = widget_class.__name__
                self.main.widget_classes[widget_class_name] = widget_class

            self.binding_info()
            return self.main
        except KeyError as e:
            traceback.print_exc()
            log.error('插件的Package.json不完整')
            log.error(e)

    def binding_info(self):
        self.main.info = Info(
            name=self.name,
            icon=self.icon,
            display_name=self.display_name,
            description=self.description,
            version=self.version,
            path=self.path
        )

    def import_module(self, path):
        filepath = os.path.join(self.path, path)

        # pyminer_paths = [path for path in sys.path if 'pyminer' in path and path not in
        #                  (self.import_path, self.extension_lib_path)]
        # for path in pyminer_paths:
        #     sys.path.remove(path)
        pyminer_paths = []

        try:
            package_name = self.name
            module_name = os.path.splitext(os.path.basename(filepath))[0]
            module = importlib.import_module(
                f'{package_name}.{module_name}')
        except Exception as e:
            traceback.print_exc()
            log.error(e)
            module = None
        # sys.path.extend(pyminer_paths)
        return module

    def load_class(self, file, class_name):
        path = os.path.join(self.path, file)
        module = self.import_module(path)
        if module:
            if hasattr(module, class_name):
                return getattr(module, class_name)
            else:
                traceback.print_exc()
                log.error(f"{file}文件中不存在{class_name}类")
        else:
            traceback.print_exc()
            log.error(f"{file}文件不存在或有误")

    def load_widget(self, widget_config):
        try:
            widget_class = self.load_class(widget_config['file'], widget_config['widget'])
            if widget_config.get('auto_insert', True):
                widget_config = self.ui_inserters[widget_config['position']](
                    widget_class, widget_config['config'])
                self.main.widgets[widget_class.__name__] = widget_config
            return widget_class
        except KeyError as e:
            traceback.print_exc()
            log.error(f"插件{self.name}的widgets配置不正确!")
            log.error(f"位置:{widget_config}")

    def create_public_interface(self, interface):
        public_interface = PublicInterface()
        for attr in dir(interface):
            obj = getattr(interface, attr)
            if not attr.startswith('_') and callable(obj):
                setattr(public_interface, attr, obj)
        return public_interface

    def reset(self):
        pass

