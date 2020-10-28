[TOC]

# pmgwidgets常用控件介绍

``` python
from pmgwidgets import {控件名}
```
用以上语句即可导入相应的控件。
控件的有关示例见pmgwidgets/tests文件夹。
## 设置控件SettingsPanel
查看本文中的示例即可。运行示例即可得到以下界面：

![](doc_figures/settings_panel.png)

### 数据结构与格式

创建这个界面只需要一个json式的数据结构，如下所示：

```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150)),
         ('number', 'height', 'How High could This Plane fly?', 12000, 'm', (10, 20000)),
         ('bool', 'sport', 'do you like sport', True),
         ('choose_box', 'plane_type', 'plane type', 'f22', ['f22', 'f18', 'j20', 'su57'],
          ['f22战斗机', 'f18战斗轰炸机', 'j20战斗机', 'su57战斗机']),
         ('color', 'color', 'Which color do u like?', (0, 200, 0))]
```
这些数据的格式为：
数据类型；数据名称；提示信息；初始值。第四位之后的其他数据为修饰信息，比如单位、范围等。

| 返回值类型                               | 1:选择器名称 | 2:数据名称 | 3：提示信息 | 4：初始值                  | 5        | 6               |
| ---------------------------------------- | ------------ | ---------- | ----------- | -------------------------- | -------- | --------------- |
| 字符串型（str）                          | 'line_edit'  | str        | str         | 初始值：str                | /        | /               |
| 整型或者浮点（int/float）字符串型（str） | 'number'     | 名称:str   | str         | int/float初始值：str       | 单位str  | 范围（min,max） |
| 布尔型（bool）                           | 'bool'       | str        | str         | bool                       | /        | /               |
| 任意类型，多选一（str）                  | 'choose_box' | str        | str         | object（任意类型）*        | 选项列表 | 选项文本列表    |
| 颜色（返回形如'#a0b89d'的颜色字符串）    | 'color'      | 'color'    | str         | tupleRGB,每位为0~255的整数 | /        |                 |
*:注意，任意类型，多选一的下拉列表中，列表可以填入任意类型。但是你所输入的初始值，必须在选项列表中存在，否则会抛出异常。

### 创建一个设置面板：

- 控件列表可以在初始化的时候传入，像这样：

```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel(views=views, layout_dir='v')
```

- 控件列表也可以在初始化完成之后传入：

```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel()
sp.set_items(views)
```

写法与初始化时相同。

- `set_items`可以多次调用。如果调用的时候设置面板不为空，那么之前的设置项都会被清空。

### 获取其上的控件

调用`get_ctrl(ctrl_name:str)`方法,可以获取其上的控件。

如：

```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel(views=views, layout_dir='v')
name_widget = sp.get_ctrl('name')
```

- 注意：如果控件名称不存在，则返回None。注意做好类型判断。

### 获取值

#### 获取单个控件值

获取控件之后，调用控件的set_value方法。
```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel(views=views, layout_dir='v')
name_widget = sp.get_ctrl('name')
name_widget.get_value()
```


#### 获取整体值

调用SettingsPanel的get_value()方法，可以返回一个字典。键就是以上表格的“数据名称”列，返回的是相应的值。

如果未做任何改动，那么返回的值就是初始值，也就是表格“初始值”列的内容。

比如之前所述的views列表输入的初始值，最终得出的结果是这样的dict：

```python
values = sp.get_value()
values = {'name': 'hzy', 'age': 88.0, 'height': 12000.0, 'sport': True, 'plane_type': 'f22', 'color': (0, 200, 0)}
```

### 设置值

比如之前所述的views列表输入的初始值，最终得出的结果是这样的dict：

```python
views = [('line_edit', 'name', 'What\'s your name?', 'James'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel(views=views, layout_dir='v')
name_widget = sp.get_ctrl('name')
name_widget.set_value("John")
```

set_value方法传入的参数，类型必须与初始值相同。

### 设置控件的参数

调用`set_params(*params)`方法。

params指的是从表格的‘初始值’列之后的几项。比如选择菜单的选项、数据型输入框的范围。

控件的参数指的就是从第5项开始（含第5项）以后的内容。比如对于一个数值型控件：

如：

```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel(views=views, layout_dir='v')
num_widget = sp.get_ctrl('name')
if num_widget is not None:
    num_widget.set_params('years old',(10,145))

```

以上示例就是把年龄范围从0~150岁设置到了10~145岁。如果你不希望改变其他设置（比如这里的‘years old’），将原有的值重新写一遍就可以了。

- 注意：如果控件名称不存在，则返回None。注意做好类型判断。

### 禁用和启用单个控件（设置灰色）

```python
views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
         ('number', 'age', 'How old are you?', 88, 'years old', (0, 150))]
sp = SettingsPanel(views=views, layout_dir='v')
sp.get_ctrl('name').setEnabled(False) # 禁用name控件
sp.get_ctrl('name').setEnabled(True)  # 启用name控件
```


示例：

```python
import sys

from PyQt5.QtWidgets import QApplication

from pmgwidgets import SettingsPanel
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 类型；名称；显示的提示文字;初始值；//单位；范围
    views = [('line_edit', 'name', 'What\'s your name?', 'hzy'),
             ('number', 'age', 'How old are you?', 88, 'years old', (0, 150)),
             ('number', 'height', 'How High could This Plane fly?', 12000, 'm', (10, 20000)),
             ('bool', 'sport', 'do you like sport', True),
             ('choose_box', 'plane_type', 'plane type', 'f22', ['f22', 'f18', 'j20', 'su57'],
              ['f22战斗机', 'f18战斗轰炸机', 'j20战斗机', 'su57战斗机']),
             ('color', 'color', 'Which color do u like?', (0, 200, 0))]
    sp = SettingsPanel(views=views, layout_dir='v')
    sp.widgets_dic['plane_type'].set_choices(['aaa', 'vvvvv', 'xxxxxx'])
    sp.set_items(views[3:6])
    sp.show()
    sp2 = SettingsPanel(views=views, layout_dir='h')
    sp2.show()
    sp2.setMaximumHeight(30)
    val = sp.get_value()  # 返回一个字典。初始值为表格的第二列：第四列。
    print(val)
    sys.exit(app.exec_())
```



## 文件树控件
class PMGFilesTreeview(QTreeView):
### 如何插入界面
def __init__(self, initial_dir: str = '', parent=None):
initial_dir:str,初始时的路径。
parent:父控件，可以为None。
### 信号：
 - new_file_signal = pyqtSignal(str)
 新建文件信号，返回一个参数，是新建文件的绝对路径
 - new_folder_signal = pyqtSignal(str)
 新建文件夹信号，返回一个参数，是新建文件夹的绝对路径
 - delete_file_signal = pyqtSignal(str)
 删除文件或者文件夹信号，返回一个参数，是文件夹的绝对路径。
 - rename_file_signal = pyqtSignal(str, str)
 文件重命名的信号，返回两个参数，分别是重命名之前的绝对路径和重命名之后的绝对路径。

 注意：以上信号都是只有操作成功才会被触发的。**如果操作不成功（比如重命名时存在相同文件、删除文件时权限不够），那么就不会触发。**。

## 容器控件

### 流式布局控件PMFlowArea

流式布局控件为PMFlowArea，示例见tests文件夹的flow_layout_widget.py。

运行这个例子可以发现以下效果：
![](doc_figures/pmflowarea_1.png)
![](doc_figures/pmflowarea_2.png)
可以看到，布局在界面左右拖拽的时候，按钮会自动重排。
问题：控件库的按钮自动重排之前，似乎不是从0,0开始添加按钮的。
### 选项卡控件PMGTabWidget
(这里名字不对！需要改过来！！)
是选项卡控件。
选项卡控件的特点是，它的setup_ui方法中，会调用子界面的setup_ui方法。同理也适用于bind_events。
### 可停靠控件PMGDockWidget
额外定义了raise_into_view的方法，调用这方法时可以保证此控件提升到窗口最顶端。
[TODO]:需要考虑将窗口也增设进来！

## 相关函数和方法
### 文件操作
#### rename_file(prev_absolute_path:str, new_absolute_path:str)->bool
重命名文件或者文件夹
prev_absolute_path:之前的绝对路径
new_absolute_path:新的绝对路径
返回值：True为操作成功，False为不成功（比如已有文件或者文件夹与新的名称重名）
#### move_to_trash（path:str）->bool
path:要移到回收站的文件夹的绝对路径。
返回值：True为操作成功，False为不成功。
### 执行系统命令
[!TODO]
#### run_command_in_terminal(打开系统终端并在其中执行命令。)
在终端命令行中运行命令。
```
from pmgwidgets import run_command_in_terminal


def test_run_in_terminal():
    import time
    run_command_in_terminal('dir', close_mode='no')
    time.sleep(1)
    run_command_in_terminal('dir', close_mode='wait_key')
    time.sleep(1)
    run_command_in_terminal('dir', close_mode='auto')


test_run_in_terminal()
```
close_mode的意思时命令执行完之后终端怎么做。当其为‘no'的时候，终端不退出，可以输入命令继续执行下一条；显示为'wait_key'的时候，终端等待按任意键退出；显示为‘auto’的时候，终端执行完之后就退出——所以执行dir一类秒完成的命令，就会闪现一下，然后便不见了。

# pmgwindows常用控件介绍
