import os
import sys
import importlib
import json
from collections import namedtuple
from pyminer_new.extensions.extensions_manager import log
from pyminer_new.pmutil import get_root_dir

# package.json大概结构
# {
#     "name":...,
#     "display_name":...,
#     "version":...,
#     "description":"...",
#     "icon":"..."
#     "interface":{
#         "file":"",
#         "interface":""
#     },
#     "widgets":[
#         {
#             "file":"",
#             "widget":"",
#             "position":"..."
#             "config":{

#             }
#         }
#     ],
#     "requirements":[
#         {
#             "name":"",
#             "version":""
#         }
#     ]
# }
# 当position为new_tab,config包含:
# name:新选项卡名称
# 当position为tab_选项卡ObjectName,config为空
# 当position为subwindow,config包含:
# name:子窗体名称
# 当position为funcion,config包含:
# file:文件名
# function_name:文件内安装插件的函数名

BASEDIR = get_root_dir()

Info=namedtuple('Info',['icon','name','display_name','version','description','path'])

class ExtensionLoader:
    def load(self,file,ui_inserters):
        self.package=json.load(file)
        self.ui_inserters=ui_inserters
        try:
            self.name=self.package['name']
            self.display_name=self.package['display_name']
            self.version=self.package['version']
            self.description=self.package['description']
            self.icon=self.package['icon']
            self.path = os.path.join(BASEDIR, 'extensions/packages/', self.name)  # 扩展文件夹路径
            self.main=self.load_obj(
                {
                    'file':'main.py',
                    'class_name':'Extension'
                },
                'class_name'
            )
            self.interface=self.load_obj(self.package['interface'],'interface')
            if getattr(self.interface,'ui_inserters',None):
                for key in self.interface.ui_inserters:
                    self.ui_inserters[f'extension_{self.name}_{key}']=self.interface.ui_inserters[key]
            self.main.interface=self.interface
            self.main.widgets=[]
            for widget in self.package['widgets']:
                widget_obj=self.load_widget(widget)
                self.main.widgets.append(widget_obj)
            self.binding_info()
            return self.main
        except KeyError as e:
            log.error('插件的Package.json不完整')
            log.error(e)
    def binding_info(self):
        self.main.info=Info(
            name=self.name,
            icon=self.icon,
            display_name=self.display_name,
            description=self.description,
            version=self.version,
            path=self.path
        )
    
    def run_code(self,path):
        path=os.path.join(self.path,path)
        sys.path.append(self.path)  # 将模块导入路径设置为扩展文件夹,这样可以直接导入入口文件
        extension_lib_path=os.path.join(BASEDIR, 'extensions/extensionlib', self.name)
        sys.path.append(extension_lib_path)
        
        try:
            model = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        except Exception as e:
            log.error(e)
            model=None

        # 删除刚才添加的路径
        for i, path in enumerate(sys.path):
            if path == self.path or path == extension_lib_path:
                del sys.path[i]
        return model

    def load_obj(self,obj,class_name):
        if not obj:
            return None
        if not (obj.get('file') and obj.get(class_name)):
            log.error('class_name配置不完整!')
            return
        path=os.path.join(self.path,obj['file'])
        model=self.run_code(path)
        if model:
            if getattr(model,obj[class_name],None):
                return getattr(model,obj[class_name],None)()
            else:
                log.error(f"{obj['file']}文件中不存在{obj[class_name]}类")
        else:
            log.error(f"{obj['file']}文件不存在或有误")

    def load_widget(self,widget):
        widget_obj=self.load_obj(widget,'widget')
        try:
            self.ui_inserters[widget['position']].insert(widget_obj,widget['config'])
            return widget_obj
        except KeyError as e:
            log.error(f"插件{self.name}的widgets配置不正确!")
            log.error(f"位置:{widget}")
