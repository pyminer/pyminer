import os
import shutil
import sys
import json
import json.decoder
import zipfile
import importlib
import traceback
# from pyminer2.features.extensions.extensionlib import env
from pyminer2.pmutil import get_root_dir
from pyminer2.extensions.extensions_manager import log
from pyminer2.extensions.extensions_manager.ExtensionLoader import ExtensionLoader
from pyminer2.extensions.extensions_manager.UIInserter import ui_inserters

BASEDIR = get_root_dir()


class ExtensionsManager:
    '''
    扩展管理类
    '''

    def __init__(self):
        self.extensions = []  # 扩展类实例
        self.ui_inserters = ui_inserters
        self.id_ = 0  # 扩展id,动态分配的
        # self.setting_path = os.path.join(
        #     BASEDIR, 'config/extensions.json')  # 扩展配置文件位置
        self.loader = ExtensionLoader()
        self.extensions_directory = os.path.join(BASEDIR, 'extensions', 'packages')

    def load_one(self, name):
        with open(os.path.join(self.extensions_directory, name, 'package.json'), encoding='utf-8') as f:
            main = self.loader.load(f, self.ui_inserters)
        self.extensions.append(main)
        main.id_ = self.id_
        self.id_ += 1
        try:
            main.on_load()
        except Exception as e:
            traceback.print_exc()
            log.error(e)
        self.loader.reset()

    def load(self):
        '''
        加载扩展
        '''
        for package in os.listdir(self.extensions_directory):
            try:
                self.load_one(package)
            except:
                log.error(f'{package} is not a valid package')
                traceback.print_exc()
        # with open(self.setting_path, encoding='utf-8') as f:
        #     try:
        #         config = json.load(f)
        #     except json.decoder.JSONDecodeError as e:
        #         traceback.print_exc()
        #         log.error('The extensions.json is Wrong')
        #         return
        # log.assert_(len(config), 'The extensions.json is Wrong')
        # for name in config['extensions']:
        #     self.load_one(name)
        # log.log('插件加载完成!')
        

    # def load(self):
    #     # 根据扩展信息加载扩展
    #     for ext in self.extensions_info:
    #         # 加载扩展实例
    #         self.extensions.append(ext.run())

    #         if not self.extensions[-1]:
    #             log.assert_(f'扩展{ext.name}加载失败!')
    #             continue

    #         # 分配id,存储信息
    #         self.extensions[-1].id_ = self.id_
    #         self.extensions[-1].info = ext
    #         self.id_ += 1

    #         # 扩展被加载的生命周期函数
    #         try:
    #             self.extensions[-1].on_load()
    #         except Exception as e:
    #             log.error(e)

    def get_ext_by_id(self, id_):
        '''通过id获取扩展'''
        for ext in self.extensions:
            if ext.id_ == id_:
                return ext
        return None

    def get_ext_by_name(self, name):
        '''通过名称获取扩展'''
        for ext in self.extensions:
            if ext.info.name == name:
                return ext
        return None

    def uninstall(self, id_):
        '''
        卸载扩展
        '''
        ext = self.get_ext_by_id(id_)

        # 卸载生命周期函数
        try:
            ext.on_uninstall()
        except Exception as e:
            traceback.print_exc()
            log.error(e)

        # 删除扩展实例
        for i, ext_ in enumerate(self.extensions):
            if ext_ is ext:
                del self.extensions[i]
                break

        # 修改配置文件
        with open(self.setting_path, encoding='utf-8') as f:
            config = json.load(f)
        for index, c in enumerate(config['extensions']):
            if c == ext.info.name:
                del config['extensions'][index]
                break
        with open(self.setting_path, 'w', encoding='utf-8') as f:
            json.dump(config, f)

        # 最后删除扩展文件夹,注意顺序
        path = ext.info.path
        shutil.rmtree(path)

    def install(self, path):
        '''本地安装扩展'''
        try:
            # 解压扩展
            file = zipfile.ZipFile(path)
            dirname = os.path.join(BASEDIR, 'extensions/packages/',
                                   '.'.join(os.path.basename(path).split('.')[:-1]))
            extract_dir = os.path.join(
                BASEDIR, 'extensions/packages/')
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
                if not self.get_ext_by_name(i):
                    self.install_web(*i)

            # 写入配置文件
            config['extensions'].append(package['name'])
            with open(self.setting_path, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            log.error("安装失败")
            log.error(str(e))
            traceback.print_exc()
            return
        else:  # else表示没有异常的情况
            self.load_one(package['name'])

    def install_web(self, name, version=''):
        # 从插件商店安装,之后完成
        pass


extensions_manager = ExtensionsManager()
