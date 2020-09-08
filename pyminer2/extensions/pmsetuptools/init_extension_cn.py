import os
import shutil
import re
import json
import requests
from extensionshop import *

def init_extension():

    print('''pyminer2 插件开发工具
v0.1.0

 _ (`-.                _   .-')                   .-') _     ('-.    _  .-')   
 ( (OO  )              ( '.( OO )_                ( OO ) )  _(  OO)  ( \( -O )  
 _.`     \   ,--.   ,--. ,--.   ,--.)  ,-.-')  ,--./ ,--,'  (,------.  ,------.  
(__...--''    \  `.'  /  |   `.'   |   |  |OO) |   \ |  |\   |  .---'  |   /`. ' 
 |  /  | |  .-')     /   |         |   |  |  \ |    \|  | )  |  |      |  /  | | 
 |  |_.' | (OO  \   /    |  |'.'|  |   |  |(_/ |  .     |/  (|  '--.   |  |_.' | 
 |  .___.'  |   /  /\_   |  |   |  |  ,|  |_.' |  |\    |    |  .--'   |  .  '.' 
 |  |       `-./  /.__)  |  |   |  | (_|  |    |  | \   |    |  `---.  |  |\  \  
 `--'         `--'       `--'   `--'   `--'    `--'  `--'    `------'  `--' '--' 

欢迎来到 pyminer 插件开发工具页面。根据以下指引你会开发一个自己的插件！''')

    package = {}

    extension_name = input(
    '首先，我们来设置一些基本属性\n'
    '输入一个你独有的名字：'
    ).strip()

    def valid_extname(extname:str) -> bool:
        return re.match(r'\w[-\w\d_\.]')

    if not check_unique(extension_name):
        extension_name = input(
            '呃，看起来这个名字好像被用过了\n'
            '重新输入一个吧：'
        ).strip()
    package['name'] = extension_name

    if os.path.exists(extension_name):
        to_delete = input('这个文件夹已经存在了，要删掉他们吗？(y/n)')
        if to_delete.strip().lower() == 'y':
            shutil.rmtree(extension_name)
        else:
            print('程序已退出。')
            return
    os.mkdir(extension_name)

    print(
        f'很好，你的插件就叫做 {extension_name}\n'
    )

    display_name = re.sub(r'[-_.]', ' ', extension_name).capitalize()

    print(
        f'现在，看看我们提供的用于展示的名字：{display_name}。你可以更改为中文。'
    )

    satisfied = input('你觉得可以吗？(y/n)').strip()
    if satisfied.lower() != 'y':
        display_name = input(
            '好的，输入你想要的名字：'
        ).strip()
    package['display_name'] = display_name

    print(
        '\n这是这个插件的第一个版本，我们建议将版本号设置为v0.1.0。根据 Semantic Versioning\n'
        '2.0.0，这是第一个开发的版本。稍后你可以在 package.json 中修改版本号。\n'
    )
    package['version'] = 'v0.1.0'

    print(
        '很棒！我们已经做了不少事了，下一步是介绍一下你的插件，用一句话说明一下'
    )

    description = input('这个插件是').capitalize().strip()
    package['description'] = description

    print(
    '\n这是一个很棒的插件，而很棒的插件一般都有一个引人注目的图标。'
    )

    def get_icon() -> str:
        path_of_icon = input('告诉我们在哪里可以找到图标：').strip()
        if os.path.exists(path_of_icon):
            icon = os.path.basename(path_of_icon)
            shutil.copy(path_of_icon, os.path.join(extension_name, icon))
            return icon
        else:
            try:
                response = requests.get(path_of_icon)
                if response.status_code == 200:
                    icon = input('我们从链接上下载了一张图片，请设置文件名：').strip()
                    with open(os.path.join(extension_name, icon), 'wb') as f:
                        f.write(response.content)
                    return icon
                else:
                    print('出了点故障……')
                    raise Exception(f'response status {response.status_code}')
            except:
                print('我们没能拿到图标，请再试一次。')
                return ''
        return ''

    icon = ''
    while not icon:
        icon = get_icon()
    package['icon'] = icon
    print('我们成功拿到了图标。\n')

    extension_title = re.sub(r'[-_.\s]', '', extension_name.title())

    extension = extension_title+'Extension'

    print(
        f'我们要开始做点激动人心的事了，要在 main.py 里写插件的主程序。类名通常是`{extension}`.'
    )
    satisfied = input('你喜欢这个名字吗？(y/n)').strip()
    if satisfied.lower() != 'y':
        extension = input(
            '好吧，你来决定：'
        ).strip()
    package['main'] = {
        'file': 'main.py',
        'main': extension
    }
    
    interface = extension_title+'Interface'

    print(
        '\n让我们进行下一步。很多插件会提供接口，以便于其他插件增强已有的功能。接口通常定义\n'
        f'在 interface.py，但你稍后也可以进行更改。我们提供的类名是 `{interface}`'
    )
    satisfied = input('你觉得怎么样？(y/n)').strip()
    if satisfied.lower() != 'y':
        interface = input(
            '好吧，那你觉得应该是：'
        ).strip()
    package['interface'] = {
        'file': 'interface.py',
        'interface': interface
    }

    print(
        '\n还要，插件通常会有很多控件，用户可以操纵这些控件。相信我，这不难，我们开始吧！'
    )
    
    widget_instances = []
    widget_classes = []

    def new_widget() -> dict:
        widget = {}

        print(
            '\n有三种控件可以添加到主窗口，可停靠窗口（dock window），工具栏（toolbar）和\n'
            '工具栏内的按钮（button）'
        )
        def select() -> int:
            index = input('选择其中一个 (1/2/3): ').strip()
            if index not in ('1', '2', '3'):
                return select()
            else:
                return int(index)-1

        widget_type = select()

        filename = input('\n你准备在哪个文件写这个控件？\n文件名：').strip()
        while not re.match(r'\w[_\w\d]*[\w\d]', filename):
            filename = input('呃，文件名不合法，请重新输入：').strip()

        widget["file"] = filename

        def config_dock_window(widget:dict) -> dict:
            print(
                '\n很不错，马上你就能创建一个可停靠窗体，你要告诉我们三件事。'
            )
            widget['config'] = config = {}
            config['name'] = input('首先，一个唯一的标识名：').strip()
            config['text'] = input('其次，窗体标题文字：').strip()
            print(
                '第三个参数指定了窗体默认加载的位置，可选地有 left, right, top 和 bottom'
            )
            config['side'] = input('你选择：').strip()

        def config_toolbar(widget:dict) -> dict:
            print(
                '\n很不错，马上你就能创建一个工具栏，你要告诉我们两件事。'
            )
            widget['config'] = config = {}
            config['name'] = input('首先，一个唯一的标识名：').strip()
            config['text'] = input('其次，工具栏选项卡文字：').strip()

        def config_button(widget:dict) -> dict:
            print(
                '\n很不错，马上你就能创建一个工具栏按钮，你要告诉我们两件事。'
            )
            widget['config'] = config = {}
            config['name'] = input('首先，一个唯一的标识名：').strip()
            config['toolbar'] = input('其次，你想加在哪个工具栏？').strip()

        widget_types = ('DockWindow', 'Toolbar', 'Button')
        widget_positions = ('new_dock_window', 'new_toolbar', 'append_to_toolbar')

        widget_funcs = {
            'new_dock_window': config_dock_window,
            'new_toolbar': config_toolbar, 
            'append_to_toolbar': config_button
        }

        print(f'\n这个控件的类名按照规范应该是 YourName{widget_types[widget_type]}.')
        class_name = input('请输入类名：').strip()
        widget['widget'] = class_name

        widget["position"] = widget_positions[widget_type]

        print(
            '\n还有一件事很重要，你想让程序在加载插件时自动插入这个控件吗？如果是的话，这意味着\n'
            '你不需要创建它的实例，我们会自动为你创建，并且添加到主界面，而你可以通过插件类的`widgets`\n'
            '属性来访问它。否则，你需要自行创建实例，你可以自行决定何时添加这个控件。通过 `widget_classes`\n'
            '属性访问它的类'
        )
        auto_insert = input('自动插入 (y/n)').strip()
        widget['auto_insert'] = auto_insert.lower() == 'y'

        def underscore(s:str):
            return re.sub( r"([A-Z])", r"_\1", s)

        if widget['auto_insert']:
            widget_instances.append(f'self.{underscore(class_name).lower()} = self.widgets["{class_name}"]\n')
        else:
            widget_classes.append(f'self.{class_name} = self.widget_classes["{class_name}"]\n')

        widget_funcs[widget["position"]](widget)

        return widget

    package['widgets'] = []

    while input('\n你想要添加一个控件吗？(y/n)').strip().lower()=='y':
        package['widgets'].append(new_widget())

    print(
        '\n有时候你会想要访问其他控件的接口，请告诉我们有哪些。'
    )
    package['requirements'] = []
    requirement = input('按回车忽略：')

    if requirement:
        interfaces_dir = os.path.join(extension_name, 'interfaces')
        os.mkdir(interfaces_dir)

    while requirement:
        try:
            text = get_interface(requirement)
            with open(os.path.join(interfaces_dir, requirement+'.py'), 'w') as f:
                f.write(text)
        except Exception as e:
            print(f'出现了一些错误 ({e}), 请重新尝试')
        else:
            package['requirements'].append(requirement)
        finally:
            requirement = input('输入一个新依赖')

    with open(os.path.join(extension_name, 'interface.py'), 'w') as f:
        f.write(
            '# Auto generated by pyminer2 extension develop tools\n'
            '\n'
            'from pmsetuptools.extbase import BaseInterface\n'
            '\n'
            f'class {interface}(BaseInterface):\n'
            '    pass\n'
        )
    
    with open(os.path.join(extension_name, 'main.py'), 'w') as f:
        f.write(
            '# Auto generated by pyminer2 extension develop tools\n'
            '\n'
            'from pmsetuptools.extbase import BaseExtension\n'
            '\n'
            f'class {extension}(BaseExtension):\n'
            '    def on_load(self):\n        '
            f'{"        ".join(widget_instances)}\n        '
            f'{"        ".join(widget_classes)}\n\n'
            '    def on_install(self):\n'
            '        pass\n\n'
            '    def on_uninstall(self):\n'
            '        pass\n'
        )

    with open(os.path.join(extension_name, 'package.json'), 'w') as f:
        f.write(json.dumps(package, indent=2))

    files = {'main.py', 'interface.py'}

    for widget in package['widgets']:
        if widget['file'] in files:
            with open(os.path.join(extension_name, widget['file']), 'a') as f:
                f.write(
                    '\n'
                    'from PyQt5.QtWidgets import QWidget\n'
                    '\n'
                    f'class {widget["widget"]}(QWidget):\n'
                    '        pass\n'
                )
        else:
            with open(os.path.join(extension_name, widget['file']), 'w') as f:
                f.write(
                    '# Auto generated by pyminer2 extension develop tools\n'
                    '\n'
                    'from PyQt5.QtWidgets import QWidget\n'
                    '\n'
                    f'class {widget["widget"]}(QWidget):\n'
                    '        pass\n'
                )
        files.add(widget['file'])

    print(
        f'恭喜你，你已全部完成！你可以在文件夹 {extension_name} 中看到插件的内容。你还能找\n'
        '到一个 interfaces 子文件夹，如果你声明了依赖关系的话。请不要套修改此文件夹内的任何\n'
        '文件，因为打包的时候会忽略此文件夹。也不要导入这个文件夹的任何内容，你应该把它看作\n'
        '是一个文档，在这里你可以了解如何使用这些接口。\n\n'
        '现在，开始你真正的插件开发之旅吧！'
    )
