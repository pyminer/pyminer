import importlib
import json
import json.decoder
import logging
import os
import shutil
import sys
import time
import zipfile

import utils
from lib.extensions.extensions_manager.ExtensionLoader import ExtensionLoader
from lib.extensions.extensions_manager.UIInserter import ui_inserters
from .vermanager import VersionsManager

logger = logging.getLogger('extensionmanager')
logger.setLevel(logging.DEBUG)


class ExtensionsManager:
    """
    扩展管理类
    """

    def __init__(self):
        self.extensions = {}  # 扩展类实例
        self.ui_inserters = ui_inserters
        self.id_ = 0  # 扩展id,动态分配的
        self.setting_path = os.path.join(
            utils.get_root_dir(), 'configuration', 'extensions.json')  # 扩展配置文件位置
        if not os.path.exists(self.setting_path):
            raise FileNotFoundError(self.setting_path)
        try:
            with open(self.setting_path, 'r') as f:
                self.setting = json.load(f)
        except:
            logger.warn('extension.json 已损坏')
            self.setting = {}
        self.loader = ExtensionLoader(self)
        # self.extensions_directory = os.path.join(
        #     utils.get_root_dir(), 'extensions', 'packages')
        self.extensions_directory = os.path.join(
            utils.get_root_dir(), 'packages')
        self.vermanager = VersionsManager()

    def enable_extension(self, name):
        if name in self.setting:
            self.setting[name]['enabled'] = True
        else:
            self.load(name)
            self.setting[name] = {'enabled': True}

    def disable_extension(self, name):
        self.setting[name]['enabled'] = False
        self.unload(name)

    def load(self, name):
        with open(os.path.join(self.extensions_directory, name, 'package.json'), encoding='utf-8') as f:
            main = self.loader.load(f, self.ui_inserters)
        self.extensions[main.info.name] = main
        main.id_ = self.id_
        self.id_ += 1
        self.loader.reset()

    def load_from_extension_folder(self, callback):
        """
        加载扩展
        """
        ext_load_status = {}
        ext_path = os.path.join(utils.get_root_dir(), 'configuration', 'extensions.json')
        with open(ext_path) as f:
            ext_dict = json.load(f)
        packages = ext_dict.keys()
        ext_load_status['ext_count'] = len(packages)
        ext_load_status['loaded'] = 0
        for package in packages:
            t0 = time.time()
            ext_load_status['loaded'] += 1
            if not os.path.isdir(os.path.join(self.extensions_directory, package)):
                logger.debug(f'{package} is not dir, ignored')
            elif package in self.setting:
                if self.setting[package].get('enabled', True):
                    self.setting[package] = {'enabled': True}
                    ext_load_status['ext_name'] = package
                    try:
                        logger.info(f'load extension {package}')
                        self.load(package)
                    except ModuleNotFoundError as e:
                        raise e
                    except BaseException:
                        logger.error(
                            f'{package} is not a valid package', exc_info=True)
            elif package not in self.setting:
                self.setting[package] = {'enabled': True}
                ext_load_status['ext_name'] = package
                try:
                    logger.info(f'load extension {package} for the first time')
                    self.load(package)
                except BaseException:
                    logger.error(
                        f'{package} is not a valid package', exc_info=True)
                pass
            if callable(callback):
                callback(ext_load_status)
            t1 = time.time()
            logger.info(f'boot time elapsed for {str(package)} : {t1 - t0:f} s')

    def get_extension(self, name):
        """通过名称获取扩展"""
        return self.extensions.get(name, None)

    def unload(self, name):
        ext = self.extensions[name]
        # 卸载生命周期函数
        try:
            ext._on_close()
        except Exception as e:
            logger.error(e, exc_info=True)
        del self.extensions[name]

    def uninstall(self, name):
        """
        卸载扩展
        """
        ext = self.get_extension(name)

        # 卸载生命周期函数
        try:
            ext._on_uninstall()
        except Exception as e:
            logger.error(e, exc_info=True)

        # 删除扩展实例
        del self.extensions[name]

        # 修改配置文件
        with open(self.setting_path, encoding='utf-8') as f:
            config = json.load(f)
        for index, c in enumerate(config['extensions']):
            if c['name'] == ext.info.name:
                del config['extensions'][index]
                break
        with open(self.setting_path, 'w', encoding='utf-8') as f:
            json.dump(config, f)

        # 最后删除扩展文件夹,注意顺序
        path = ext.info.path
        shutil.rmtree(path)

    def install(self, path):
        """本地安装扩展"""
        try:
            # 解压扩展
            file = zipfile.ZipFile(path)
            dirname = os.path.join(utils.get_root_dir(), 'packages',
                                   '.'.join(os.path.basename(path).split('.')[:-1]))
            extract_dir = os.path.join(
                utils.get_root_dir(), 'packages')
            file.extractall(extract_dir)
            file.close()

            # 配置文件
            with open(self.setting_path, encoding='utf-8') as f:
                config = json.load(f)
            # 扩展内的package.json配置文件
            with open(os.path.join(dirname, 'package.json'), encoding='utf-8') as f:
                package = json.load(f)
            # 自动安装依赖
            for i in package.get('requirements', []):
                if not self.get_extension(i):
                    self.install_web(*i)

            # 写入配置文件
            config['extensions'].append({
                'name': package['name'],
                'enable': True
            })
            with open(self.setting_path, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            logger.error(f"安装失败 {e}", exc_info=True)
            return
        else:  # else表示没有异常的情况
            self.load(package['name'])

    def download(self, name, version=''):
        # 从插件商店安装,之后完成
        pass

    def stop(self):
        with open(self.setting_path, 'w') as f:
            json.dump(self.setting, f, indent=2)

    def refresh(self, id_):
        ext = self.get_extension(id_)
        name = ext.info.name
        self.unload(name)
        with open(os.path.join(ext.info.path, 'package.json'), 'r', encoding='utf-8') as f:
            main_config = json.load(f).get(
                'main', {'file': 'main.py', 'main': 'Extension'})
        module_name = f"{name}.{main_config['file'].split('.')[0]}"
        importlib.reload(sys.modules[module_name])
        self.load(name)


extensions_manager = ExtensionsManager()
