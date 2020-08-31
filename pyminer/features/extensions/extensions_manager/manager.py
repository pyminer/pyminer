import os
import shutil
import sys
import json
import json.decoder
import zipfile
import importlib
#from pyminer.features.extensions.extensionlib import env
from pyminer.pmutil import get_main_window


BASEDIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))))


def _log(text):
    '''日志输出text'''
    # 放在函数体中防止循环引用,接下来的也是

    get_main_window().slot_flush_console('info', 'Extension')


def _assert_(boolean, text):
    '''
    boolean:bool
    text:str
    若bool为false,以异常级输出text
    '''
    if not boolean:
        get_main_window().slot_flush_console(
            'error', 'Extension', 'Error:'+str(text))


class ExtensionInfo:
    '''
    扩展信息
    '''

    def __init__(self, name,display_name, version, description, icon):
        '''
        name:扩展名称
        version:扩展版本
        description:扩展描述
        icon:扩展图标
        '''
        self.name = name
        self.version = version
        self.description = description
        self.main = 'main.py'  # 扩展入口文件
        self.icon = icon
        self.display_name=display_name
        self.path = os.path.join(
            BASEDIR, 'features/extensions/packages/', self.name)  # 扩展文件夹路径

    def run(self):
        sys.path.append(self.path)  # 将模块导入路径设置为扩展文件夹,这样可以直接导入入口文件
        sys.path.append(os.path.join(BASEDIR,'features/extensions/',self.name))
        main = importlib.import_module('main')

        # 删除刚才添加的路径
        for i, path in enumerate(sys.path):
            if path == self.path:
                del sys.path[i]

        # 获取扩展类
        if getattr(main, 'Extension', False):
            return getattr(main, 'Extension')()
        else:
            _assert_(False, f'扩展{self.name}没有创建入口Extension类')


class ExtensionsManager:
    '''
    扩展管理类
    '''

    def __init__(self):
        self.extensions = []  # 扩展类实例
        self.extensions_info = []  # ExtensionInfo实例
        self.id_ = 0  # 扩展id,动态分配的
        self.setting_path = os.path.join(
            BASEDIR, 'config/extensions.json')  # 扩展配置文件位置

    def load_setting(self):
        '''
        加载扩展配置文件
        '''
        with open(self.setting_path, encoding='utf-8') as f:
            try:
                config = json.load(f)
            except json.decoder.JSONDecodeError as e:
                _assert_(False, 'The extensions.json is Wrong')
                return
        _assert_(len(config), 'The extensions.json is Wrong')
        self.extensions_info.clear()
        for extension_info in config['extensions']:
            # **表示将字典作为参数传递
            # 创建扩展信息实例
            self.extensions_info.append(ExtensionInfo(**extension_info))

    def load(self):
        # 根据扩展信息加载扩展
        for ext in self.extensions_info:
            # 加载扩展实例
            self.extensions.append(ext.run())

            if not self.extensions[-1]:
                _assert_(f'扩展{ext.name}加载失败!')
                continue

            # 分配id,存储信息
            self.extensions[-1].id_ = self.id_
            self.extensions[-1].info = ext
            self.id_ += 1

            # 扩展被加载的生命周期函数
            try:
                self.extensions[-1].on_load()
            except Exception as e:
                _assert_(False, e)

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
            _assert_(False, e)

        # 删除扩展实例
        for i, ext_ in enumerate(self.extensions):
            if ext_ is ext:
                del self.extensions[i]
                break

        # 修改配置文件
        with open(self.setting_path, encoding='utf-8') as f:
            config = json.load(f)
        for index, c in enumerate(config['extensions']):
            if c['name'] == ext.info.name:
                del config['extensions'][index]
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
            dirname = os.path.join(BASEDIR, 'features/extensions/packages/',
                                   '.'.join(os.path.basename(path).split('.')[:-1]))
            extract_dir = os.path.join(
                BASEDIR, 'features/extensions/packages/')
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
            # 删除依赖这个键
            try:
                del package['requirements']
            except:
                pass
            
            # 写入配置文件
            config['extensions'].append(package)
            with open(self.setting_path, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            _assert_(False, "安装失败")
            _assert_(False, str(e))
            return
        else:  # else表示没有异常的情况
            # 重新加载扩展
            self.load_setting()
            for ext in self.extensions_info:
                # 只重新加载新安装的扩展
                if ext.name == package['name']:
                    self.extensions.append(ext.run())
                    try:
                        self.extensions[-1].on_install()
                    except Exception as e:
                        _assert_(False, e)
                        raise e
                    self.extensions[-1].id_ = self.id_
                    self.extensions[-1].info = ext
                    self.id_ += 1
                    try:
                        self.extensions[-1].on_load()
                    except Exception as e:
                        _assert_(False, e)
                        raise e
                    break

    def install_web(self, name, version=''):
        # 从插件商店安装,之后完成
        pass


extensions_manager = ExtensionsManager()
