ExtensionLib:

## 基本方法

def get_interface(self, name: str) -> BaseInterface:
获取名为`name`的插件的公共接口（由interface定义）

- Args:
- name:

Returns: Interface，须继承BaseInterface,并且在插件的main.py文件中定义。

### 在界面的可停靠窗口上插入控件


def insert_widget(self, widget, insert_mode, config=None):

在主界面上插入一个控件。
Args:
- widget:  被插入的控件（继承QWidget）
- insert_mode:  插入方式（字符串描述）
- config:  插入的位置等。

Returns:

### 获取主程序路径

def get_main_program_dir(self):

- 获取主程序的根目录
      

## UI子类（图形界面方法）

class UI():
### 获取工具栏方法
@staticmethod
def get_toolbar(toolbar_name: str) -> 'PMGToolBar':
获取工具栏

Args:
- toolbar_name:工具栏名称

Returns: 当前工具栏。若工具栏不存在，则返回None。

### 获取工具栏上的控件的方法
@staticmethod
def get_toolbar_widget(toolbar_name: str, widget_name: str) -> Optional['QWidget']:
获取工具栏上的控件（按钮等）

Args:
- toolbar_name:工具栏名称
- widget_name:工具栏上的控件名称

Returns: QWidget，工具栏上的控件。如果没有则返回None。


@staticmethod
def add_translation_file(file_name: str) -> None:
添加翻译文件
TODO：这个功能不太好，建议去掉，直接用QApplication里的方法来添加。
Args:
file_name:
Deprecated!!
Returns:
### 获取主界面的位置和尺寸
@staticmethod
def get_main_window_geometry() -> 'QRect':
获取主界面的尺寸

Returns: QRect(x,y,w,h),亦即MainWindow的geometry。
### 将当前的停靠窗口提升到可见位置
@staticmethod
def raise_dock_into_view(dock_widget_name: str) -> None:
将界面上的控件提升到可视的位置

Args:
dock_widget_name:

Returns:
### 获取默认字体文件的路径    
@staticmethod
def get_default_font() -> str:

获取默认字体文件的位置

Returns: Filepath of font.
### 切换工具栏
@staticmethod
def switch_toolbar(toolbar_name: str, switch_only: bool = True):
切换工具栏

Args:
- toolbar_name:
- switch_only: 如果为True，那么在调用时只会切换工具栏，若当前的工具栏名称为`name`，则调用多次，也不会改变当前工具栏的显示状态。为False的时候，若当前工具栏名称为`name`，那么就会改变显示状态，亦即原先显示的隐藏，原先隐藏的显示。

Returns: None
## 信号相关
class Signal():
### 注意事项：
PyMiner采用QtPy做PySide2和PyQt5之间的转换。目前，PyMiner使用的是PyQt5，因此返回类型为pyqtSignal。未来移植到PySide2平台后，则为Signal.
### 获取主界面关闭事件
@staticmethod
def get_close_signal() -> Signal:
获取关闭信号

Returns: 主界面的窗口关闭信号


### 获取窗口位置、尺寸改变的信号
@staticmethod
def get_window_geometry_changed_signal():

获取窗口位置和尺寸变化的信号

Returns    

### 获取布局加载完成信号
@staticmethod
def get_layouts_ready_signal():
"""
获取布局加载完毕的事件

Returns:

"""
### 获取控件加载完毕的信号
@staticmethod
def get_widgets_ready_signal():
获取控件加载完毕的事件

Returns:

### 获取事件绑定完毕的信号
@staticmethod
def get_events_ready_signal():
获取界面信号和事件绑定完毕的事件。

Returns:

### 获取设置被改变的信号
@staticmethod
def get_settings_changed_signal() -> 'Signal':
获取设置发生变化时的事件。

Returns: 主界面设置发生变更时的信号
## 程序

        class Program():
### 添加设置面板
@staticmethod
def add_settings_panel(text: str, panel_content: List[Tuple[str, str]]):
添加一个设置面板到主界面的设置栏。
要求就是设置栏的语法符合pmgpanel语法。
Args:
text:
panel_content:

Returns:

### 在日志面板显示日志
@staticmethod
def show_log(level: str, module: str, content: str) -> None:

调用——PluginInterface.show_log('info','CodeEditor','新建文件')
输出——2020-08-29 23:43:10 hzy INFO [CodeEditor]:新建文件
Args:
level: 类型，比如‘info’
module: 模块。比如'Jupyter'
content: 内容。自定义的字符串

Returns:

### 获取主程序路径
@staticmethod
def get_main_program_dir():
获取主程序路径

Returns:

### 添加翻译文件
@staticmethod
def add_translation(locale: str, text: dict):
"""

Args:
locale:
text:

Returns:

"""
return pmlocale.add_locale(locale, text)

### 翻译
@staticmethod
def _(text):

Args:
text:

Returns:


### 获取设置
@staticmethod
def get_settings() -> Dict[str, str]:
"""

Returns:

"""

### 设置当前工作路径
@staticmethod
def set_work_dir(work_dir: str) -> None:

设置当前工作路径

Args:
work_dir:

Returns:

"""

### 获取当前工作路径

@staticmethod
def get_work_dir() -> str:

获取当前工作路径

Returns:
### 运行Python文件命令
@staticmethod
def run_python_file(file_path: str):
"""
运行Python文件命令
TODO: Write a shell console into pyminer.

Args:
file_path:

Returns: None

## 数据服务相关

class Data():
### 删除变量
@staticmethod
def delete_variable(var_name: str, provider: str = 'unknown'):
"""
删除变量
Args:
var_name:
provider:

Returns:

"""
data_manager.delete_data(var_name, provider)

### 获取所有的变量名
@staticmethod
def get_all_variable_names() -> List[str]:

获取所有的变量名

Returns:

### 获取所有非保留的变量的名称
@staticmethod
def get_all_public_variable_names() -> List[str]:

获取所有非保留的变量的名称

Returns:

### 获取全部变量（包含保留类型）
@staticmethod
def get_all_variables() -> Dict[str, object]:

获取全部变量（包含保留类型，可能返回结果比较乱，需要审慎使用）

Returns:

### 获取所有的外部可访问变量。
@staticmethod
def get_all_public_variables() -> Dict[str, object]:

获取所有的外部可访问变量。

Returns:

### 添加数据改变时触发的回调函数
@staticmethod
def add_data_changed_callback(callback: Callable[[str, str], None]) -> None:

添加数据改变时触发的回调函数

Args:
callback:

Returns:None

### 移除数据改变时触发的回调函数
@staticmethod
def remove_data_changed_callback(callback: Callable):


### 添加数据删除时触发的回调函数
@staticmethod
def add_data_deleted_callback(deletion_callback: Callable[[str, str], None]):
绑定的函数，要求其输入的函数参数为两个。

Args:
deletion_callback:

Returns:


​    
@staticmethod
def get_all_vars_of_type(types: Union[object, Tuple]):

按照类型过滤变量。

Args:
types:

Returns:


@staticmethod
def var_exists(var_name: str):

判断var_name对应的变量是否存在
Args:
var_name:

Returns:


@staticmethod
def set_var(varname: str, variable, provider='unknown', **info):

Args:
varname:
variable:
provider:
\*\*info:

Returns: None

@staticmethod
def get_var(var_name: str) -> object:

Args:
var_name:

Returns:

    
@staticmethod
def update_var_dic(var_dic: dict, provider: str, metadata_dic: dict = None):

Args:
var_dic:
provider:
metadata_dic:

Returns:

    
@staticmethod
def get_metadata(varname: str) -> dict:
    """

Args:
varname:

Returns:

"""
return data_manager.get_data_info(varname)
    
@staticmethod
def get_all_metadata() -> dict:
"""

Returns:

"""
d = {k: v for k, v in data_manager.metadataset.items()}
return d

