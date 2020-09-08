import os
import shutil
import re
import json
import requests
from extensionshop import *

def init_extension():

    print('''pyminer2 extension develop tools
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

Welcome to extension setup tools for pyminer. Following the guidance you will 
develop your own extension.''')

    package = {}

    extension_name = input(
    'First, let\'s define your extension.\n'
    'Input a unique name: '
    ).strip()

    def valid_extname(extname:str) -> bool:
        return re.match(r'\w[-\w\d_\.]')

    if not check_unique(extension_name):
        extension_name = input(
            'Uhh, it looks like that some one has used this name.\n'
            'Please re-input: '
        ).strip()
    package['name'] = extension_name

    if os.path.exists(extension_name):
        to_delete = input('This folder already exists, delete them? (y/n)')
        if to_delete.strip().lower() == 'y':
            shutil.rmtree(extension_name)
        else:
            print('The program has exited')
            return
    os.mkdir(extension_name)

    print(
        f'Well, your extension will be marked by the unique name {extension_name}\n'
    )

    display_name = re.sub(r'[-_.]', ' ', extension_name).capitalize()

    print(
    f'Now, we have prepare a name for display like this: {display_name}.'
    )

    satisfied = input('Do you satisfy with this? (y/n)').strip()
    if satisfied.lower() != 'y':
        display_name = input(
            'Okay, now input the name for display as you want: '
        ).strip()
    package['display_name'] = display_name

    print(
    '\nIt\'s the first version of this extension, so we suggest the version to be\n'
    'v0.1.0, which usually is, according to the Semantic Versioning 2.0.0, the\n'
    'the initial development release version. You can easily modify the version\n'
    'later in package.json\n'
    )
    package['version'] = 'v0.1.0'

    print(
    'Great! We\'ve done many things. The next step is to introduce your extension,\n'
    'Let\'s make a simple one-line description.'
    )

    description = input('This extension is ').capitalize().strip()
    package['description'] = description

    print(
    '\nIt\'s a definitely wonderful extension, and a great extension always has an\n'
    'attractive icon. '
    )

    def get_icon() -> str:
        path_of_icon = input('Tell us where to find the icon: ').strip()
        if os.path.exists(path_of_icon):
            icon = os.path.basename(path_of_icon)
            shutil.copy(path_of_icon, os.path.join(extension_name, icon))
            return icon
        else:
            try:
                response = requests.get(path_of_icon)
                if response.status_code == 200:
                    icon = input('We got an image from the url, please tell us the filename: ').strip()
                    with open(os.path.join(extension_name, icon), 'wb') as f:
                        f.write(response.content)
                    return icon
                else:
                    print('Something went wrong...')
                    raise Exception(f'response status {response.status_code}')
            except:
                print('We failed to obtain the icon, please to try again.')
                return ''
        return ''

    icon = ''
    while not icon:
        icon = get_icon()
    package['icon'] = icon
    print('We\'ve successfully got the icon.\n')

    extension_title = re.sub(r'[-_.\s]', '', extension_name.title())

    extension = extension_title+'Extension'

    print(
        'We are starting to do some great things! We will write the main class of the\n'
        f'extension in main.py. Usually the class will be `{extension}`.'
    )
    satisfied = input('Would you like it? (y/n)').strip()
    if satisfied.lower() != 'y':
        extension = input(
            'Okay, define it yourself: '
        ).strip()
    package['main'] = {
        'file': 'main.py',
        'main': extension
    }
    
    interface = extension_title+'Interface'

    print(
        '\nLet\'s move to the next step. Many extension have an interface such that\n'
        'other extensions may ask for to enhance the functions of your extension.\n'
        'Usually we define the interface in interface.py, but you can change it\n'
        f'later. We also prepared the name of interface class `{interface}`'
    )
    satisfied = input('Would you like it? (y/n)').strip()
    if satisfied.lower() != 'y':
        interface = input(
            'Okay, define it yourself: '
        ).strip()
    package['interface'] = {
        'file': 'interface.py',
        'interface': interface
    }

    print(
        '\nWhat\'s more, an excellent extension usually contains many widgets where\n'
        'users can operate. It won\'t be a hard job, let\'s begin!'
    )
    
    widget_instances = []
    widget_classes = []

    def new_widget() -> dict:
        widget = {}

        print(
            '\nThere are three types of widget that can be add to the main GUI program,\n'
            'which are a dock window, a toolbar or a button inside a toobar'
        )
        def select() -> int:
            index = input('Select one of them (1/2/3): ').strip()
            if index not in ('1', '2', '3'):
                return select()
            else:
                return int(index)-1

        widget_type = select()

        filename = input('\nIn which file do you plan to write this widget?\nIn file: ').strip()
        while not re.match(r'\w[_\w\d]*[\w\d]', filename):
            filename = input('Uhh, this is an invalid filename, please re-input: ').strip()

        widget["file"] = filename

        def config_dock_window(widget:dict) -> dict:
            print(
                '\nGood, you will create a new dock window when finishing this procedure. It\'s not\n'
                'complicated. You need define only three things.'
            )
            widget['config'] = config = {}
            config['name'] = input('First, the unique object name: ').strip()
            config['text'] = input('Second, the text displayed on the dock window title: ').strip()
            print(
                'The third thing is `side`, which indicates the dock window will be on default docked\n'
                'to which side. A valid value of this term can be left, right, top and bottom'
            )
            config['side'] = input('Your selection is: ').strip()

        def config_toolbar(widget:dict) -> dict:
            print(
                '\nGood, you will create a new toolbar when finishing this procedure. It\'s very easy.\n'
                'You need define only two things.'
            )
            widget['config'] = config = {}
            config['name'] = input('First, the unique object name: ').strip()
            config['text'] = input('Second, the text displayed on the toolbar label: ').strip()

        def config_button(widget:dict) -> dict:
            print(
                '\nGood, you will add a new button when finishing this procedure. It\'s very easy.\n'
                'You need define only two things.'
            )
            widget['config'] = config = {}
            config['name'] = input('First, the unique object name: ').strip()
            config['toolbar'] = input('Second, the toolbar where you would like to add the button: ').strip()

        widget_types = ('DockWindow', 'Toolbar', 'Button')
        widget_positions = ('new_dock_window', 'new_toolbar', 'append_to_toolbar')

        widget_funcs = {
            'new_dock_window': config_dock_window,
            'new_toolbar': config_toolbar, 
            'append_to_toolbar': config_button
        }

        print(f'\nA class name of this widget is suggested to be YourName{widget_types[widget_type]}.')
        class_name = input('You would like to name the class as: ').strip()
        widget['widget'] = class_name

        widget["position"] = widget_positions[widget_type]

        print(
            '\nAnother thing is important. Do you want to insert this widget automatically\n'
            ' when the extension is loaded? If yes, this means that you don\'t need to\n'
            'instantiate the widget class and we will do it for you. We will create one\n'
            'instance and insert it to the main window. To obtain the instance, you just\n'
            'turn to the extension class and visit `widgets`. Otherwise, you can instantiate\n'
            'the class by yourself, so that you can decide the time to do so. Visit `widget_classes`\n'
            'to get the class of this widget.'
        )
        auto_insert = input('Auto insert (y/n)').strip()
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

    while input('\nWould you like to add a widget? (y/n)').strip().lower()=='y':
        package['widgets'].append(new_widget())

    print(
        '\nSometimes you would like to get access of interfaces of other extensions.\n'
        'Tell us if there is any in need.'
    )
    package['requirements'] = []
    requirement = input('Press enter to ignore: ')

    if requirement:
        interfaces_dir = os.path.join(extension_name, 'interfaces')
        os.mkdir(interfaces_dir)

    while requirement:
        try:
            text = get_interface(requirement)
            with open(os.path.join(interfaces_dir, requirement+'.py'), 'w') as f:
                f.write(text)
        except Exception as e:
            print(f'There are some errors ({e}), please try again.')
        else:
            package['requirements'].append(requirement)
        finally:
            requirement = input('Input a new requirement: ')

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
        'Congrats! The work is all done! Now you can see the extension stuffs in\n'
        f'the folder named {extension_name}. You will also find a sub folder named\n'
        'interfaces if you\'ve ever ordered an interface of other extension. Do not\n'
        'modified anything in this folder because it will be ignored when packaging.\n'
        'Do not import them as well, just take them as docs telling you how to use\n'
        'the interfaces.\n\n'
        'Now, let\'s begin the extension development!'
    )
