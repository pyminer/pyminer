from typing import Tuple

from PySide2.QtWidgets import QWidget


class PMDockObject(object):
    """
    修改：
    原先，主窗口中的各个可停靠窗口，在点击右上角关闭按钮的时候会隐藏，可以在视图菜单中打开。
    但是当控件中有on_closed_action属性，且值为‘delete’的时候，控件就会被回收。
    为了实现控件的管理，控件需要继承PMDockObject，并且需要用多继承的方式。
    注意，凡是要和一些内置事件绑定的控件，都不要用delete。


    from features.ui.generalwidgets import PMDockObject
    这个PMDockObject中定义了一些方法，作为补充。

    class PMDockObject(object):
        on_closed_action = 'hide'  # 或者'delete'。

        def raise_widget_to_visible(self, widget: 'QWidget'):
            pass

        def on_dock_widget_deleted(self):
            pass

    """
    on_closed_action = 'hide'  # 或者'delete'。

    def is_temporary(self) -> bool:
        """
        如果为True,相应的控件将在窗口关闭时删除，并且不会记忆其位置。如果为False，则相应的控件不会被删除，且其位置将被记忆。

        默认返回False。
        """
        return False

    def raise_widget_to_visible(self, widget: 'QWidget'):
        pass

    def on_dock_widget_deleted(self):
        pass

    def get_split_portion_hint(self) -> Tuple[int, int]:
        return (None, None)

    def set_extension_lib(self, extension_lib):
        """
        设置扩展库。
        :param extension_lib:
        :return:
        """
        self.extension_lib = extension_lib

    def setup_ui(self):
        pass

    def bind_events(self):
        pass

    def get_widget_text(self) -> str:
        return ''
