"""
控件插入器
作者：冰中火

这是加载UI控件的插件类。
插件导入的时候，传递的widget_class是控件的类。
1、对于新建的工具栏类、插入工具栏的控件类、插入主窗口的控件类，控件插入器直接将控件类实例化，
然后插入在由config.json中指定的位置；
2、对于对话框类，控件插入器不会将其实例化，而会将其保存在对话框类管理器中。使用时，调用相应的方法，可以显示对话框。
请注意，对话框并不是什么只能问问题，点‘确定、取消’的类。只要继承QDialog的界面都要这样处理。
以上1中所述的情况将在应用初始化时完成；而2则是动态的过程，可以在应用初始化完成后就弹出对话框进行显示。


插件导入时参数由json中的config设置项所决定。

config:是一个字典,但是现在传入的参数还远远不够。
以这个文件的json配置为例，有以下要求：
"file":声明了控件类的入口位置。一般就是在main.py之中。
position:插件插入位置。有两种选项：‘new_dock_window’和‘new_toolbar’
config:设置属性。
config.message:插件的设置信息，可以为空。
config.name:插件的名称
config.side:插件插入窗口时的位置（当position=new_dock_window时有效），有left\right\top\bottom四个选项
config.text:插件的文字。会显示在dockwidget或者工具栏上
{
    "file":"main.py",
    "widget_class":"WidgetTest",
    "position":"new_dock_window",
    "config":{
        "message":"no",
        "name":"code_editor",
        "side": "right",
        "text": "编辑器"
    }
}


插件管理器下一步的目的就是将插件尽可能不一次性的加载完，插件可以自行设置插入到程序的时间，
尽可能在主界面发出初始化完成信号之后在进行调用。
"""
from typing import TYPE_CHECKING
from pyminer2.pmutil import get_main_window

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QWidget


def get_item_coor(coors: set, pos: str):
    l = list(coors)
    if pos == 'max':
        return max(l)
    elif pos == 'min':
        return min(l)
    else:
        l = sorted(l)
        if len(l) == 1:
            return l[0]
        else:
            return l[1]


def get_dock_by_position(pos: str):
    import pyminer2.pmutil
    if not pos in {'top', 'bottom', 'left', 'right'}:
        raise Exception('dockwidget的位置须由合法字符串指定，这些字符串是：\'top\', \'bottom\', \'left\', \'right\'')
    pos_dic = {'top': ('med', 'min'), 'bottom': ('med', 'max'), 'right': ('max', 'med'), 'left': ('min', 'med')}

    x_set = set()
    y_set = set()
    x_policy, y_policy = pos_dic[pos]

    for k in pyminer2.pmutil.get_main_window().dock_widgets.keys():
        w2 = pyminer2.pmutil.get_main_window().get_dock_widget(k)
        if w2.x() >= 0:
            x_set.add(w2.x())
    x_pos = get_item_coor(coors=x_set, pos=x_policy)
    for k in pyminer2.pmutil.get_main_window().dock_widgets.keys():
        w2 = pyminer2.pmutil.get_main_window().get_dock_widget(k)
        if w2.x() == x_pos and w2.y() >= 0:
            y_set.add(w2.y())
    if 0 in y_set and len(list(y_set)) > 1:
        y_set.remove(0)

    y_pos = get_item_coor(coors=y_set, pos=y_policy)

    for k in pyminer2.pmutil.get_main_window().dock_widgets.keys():
        w2 = pyminer2.pmutil.get_main_window().get_dock_widget(k)
        if w2.x() == x_pos and w2.y() == y_pos:
            return w2


class UiInserter(dict):
    def __init__(self):
        self.update({
            'new_dock_window': self.new_dock_window,
            'new_toolbar': self.new_toolbar,
            'append_to_toolbar': self.append_to_toolbar,
            'new_dock_window_obj':self.new_dock_window_obj
        })

    def new_toolbar(self, widget_class: 'QWidget', config=None):
        from pyminer2.pmutil import get_main_window
        name = config['name']
        text = config['text']

        widget = widget_class()
        get_main_window().add_toolbar(name=name, toolbar=widget, text=text)
        return widget

    def new_dock_window(self, widget_class: 'QWidget', config=None):
        from pyminer2.pmutil import get_main_window
        ()
        dock_name = config['name']
        text = config['text']
        side = config['side']
        widget = widget_class()

        dock = get_main_window().add_widget_on_dock(dock_name=dock_name,
                                                    widget=widget, text=text, side=side)

        if side in {'top', 'bottom', 'left', 'right'}:
            import pyminer2.pmutil
            w2 = get_dock_by_position(side)
            pyminer2.pmutil.get_main_window().tabifyDockWidget(w2, dock)
            pyminer2.pmutil.get_main_window()
            dock.raise_into_view()
        return widget

    def new_dock_window_obj(self, widget: 'QWidget', config=None):
        """
        以窗口对象插入，适用于已经创建的窗口。
        :param widget:
        :param config:
        :return:
        """
        from pyminer2.pmutil import get_main_window
        ()
        dock_name = config['name']
        text = config['text']
        side = config['side']

        widget = widget
        dock = get_main_window().add_widget_on_dock(dock_name=dock_name,
                                                    widget=widget, text=text, side='left')

        if side in {'top', 'bottom', 'left', 'right'}:
            import pyminer2.pmutil
            w2 = get_dock_by_position(side)
            pyminer2.pmutil.get_main_window().tabifyDockWidget(w2, dock)
            pyminer2.pmutil.get_main_window()
            dock.raise_into_view()
        return widget

    def append_to_toolbar(self, widget_class: 'QWidget', config=None):
        from pyminer2.pmutil import get_main_window
        button_name = config['name']
        toolbar_name = config['toolbar']
        widget = widget_class()
        toolbar = get_main_window().toolbars.get(toolbar_name)
        toolbar.add_widget(button_name, widget)
        # PluginInterface.get_toolbar(toolbar_name).add_widget(
        #     button_name, widget)
        return widget


ui_inserters = UiInserter()
