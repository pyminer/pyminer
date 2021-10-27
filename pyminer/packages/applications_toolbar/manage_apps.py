import os
import json
import sys
from typing import List, Dict, Union, Optional
from widgets import assert_in


def check_package_json(dic: Dict):
    assert dic['entry_point']['type'] in ['file', 'command']


class ToolAppDesc():
    """
    作为APP描述类，里面含有App的各种信息。
    """

    def __init__(self, pkg_dic: dict, path: str):
        self.path = path
        self.name = pkg_dic['name']
        self.group = pkg_dic['group']
        self.readme_file: str = os.path.join(self.path, pkg_dic['readme'])

        self.entry_point = pkg_dic['entry_point']

        self.icon_path = os.path.join(self.path, pkg_dic['icon'])
        self.text = pkg_dic['display_name']
        self.version = pkg_dic['version']
        self.pip_packages = pkg_dic['pip_packages']

        self.start_times = 0
        self.pinned = False

    def update_status(self, status_dic: dict):
        self.start_times = status_dic['starts']
        self.pinned = status_dic['pinned']

    def get_args(self) -> List[str]:
        """
        获取命令的参数
        Returns:

        """
        if self.entry_point['type'] == 'file':
            return [sys.executable] + [os.path.join(self.path, self.entry_point['file'])] + self.entry_point['args']
        elif self.entry_point['type'] == "command":
            return self.entry_point['command']
        else:
            raise ValueError('Unrecognized app entry point type %s!' % self.entry_point['type'])

    def get_settings(self) -> Dict[str, Union[int, str]]:
        """
        获取设置信息
        Returns:

        """
        return {'starts': self.start_times, 'pinned': self.pinned}


class APPManager():
    extension_lib = None

    @classmethod
    def __new__(cls, *args):
        if not hasattr(cls, 'instance'):
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    @staticmethod
    def get_instance() -> 'APPManager':
        return APPManager.instance

    def __init__(self):
        self.apps: Dict[str, ToolAppDesc] = {}
        self.settings = {}
        self.load_settings()
        self.internal_apps_folder = os.path.join(os.path.dirname(__file__), 'apps')

    def set_extension_lib(self, extension_lib):
        self.extension_lib = extension_lib
        self.extension_lib.Signal.get_close_signal().connect(self.save_settings)

    def load_settings(self):
        """
        加载设置
        Returns:

        """
        path = os.path.join(os.path.expanduser('~'), '.pyminer', 'packages', 'applications_toolbar')
        json_path = os.path.join(path, 'settings_apps.json')
        default_json_path = os.path.join(os.path.dirname(__file__), 'settings_apps.json')

        with open(default_json_path, 'rb') as f:
            app_status = json.load(f)

        if os.path.exists(json_path):
            with open(json_path, 'rb') as f:
                try:
                    app_status.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        self.settings = app_status

    def refresh_settings(self):
        """
        刷新设置
        Returns:

        """
        self.settings['apps'] = {}
        for app_name, app in self.apps.items():
            self.settings['apps'][app_name] = app.get_settings()

    def save_settings(self):
        """
        保存设置
        Returns:

        """
        self.refresh_settings()
        path = os.path.join(os.path.expanduser('~'), '.pyminer', 'packages', 'applications_toolbar')
        if os.path.exists(path):
            json_path = os.path.join(path, 'settings_apps.json')
            with open(json_path, 'w') as f:
                json.dump(self.settings, f, indent=4)

    def load_tool_apps(self):
        """
        加载工具应用
        Returns:

        """
        info_dict = {}
        for tools_folder in self.get_app_paths():
            for subfolder in os.listdir(tools_folder):
                pkg_path = os.path.join(tools_folder, subfolder)
                pkg_json_path = os.path.join(pkg_path, 'package.json')

                if os.path.exists(pkg_json_path):
                    with open(pkg_json_path, 'rb') as f:
                        info = json.load(f)
                        check_package_json(info)
                    info_dict[info['name']] = ToolAppDesc(info, pkg_path)
        for name, app in self.apps.items():
            if name in self.settings.keys():
                app.update_status(self.settings[name])
        self.apps = info_dict
        self.refresh_settings()

    def get_app(self, app_name: str) -> Optional[ToolAppDesc]:
        """
        通过名称获取一个APP.
        Args:
            app_name:

        Returns:

        """
        try:
            assert_in(app_name, self.apps.keys())
            return self.apps[app_name]
        except AssertionError:
            return None

    def set_app_external_paths(self, paths: List[str]):
        """
        设置在外部搜索应用的路径（不包含默认路径）
        Args:
            paths:

        Returns:

        """
        self.settings['paths'] = paths

    def get_app_external_paths(self) -> List[str]:
        """
        获取所有外部的应用搜索路径
        Returns:

        """
        return self.settings['paths']

    def get_app_paths(self) -> List[str]:
        """
        获取全部应用搜索路径。第1个是内部搜索路径，后面的是外部的。
        Returns:

        """
        return [self.internal_apps_folder] + self.get_app_external_paths()

    def get_app_install_path(self, app_name) -> str:
        """
        获取app_name名称的应用的安装路径
        Args:
            app_name:

        Returns:

        """
        assert_in(app_name, self.apps.keys())
        return self.apps[app_name].path


am = APPManager()
if __name__ == '__main__':
    folder = os.path.join(os.path.dirname(__file__), 'apps')

    apps = APPManager().load_tool_apps(folder)
    print(am.load_settings())
    print(am.apps)
    print(apps)
    print(APPManager.get_instance().apps)
