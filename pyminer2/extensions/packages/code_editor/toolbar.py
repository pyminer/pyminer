from pyminer2.ui.generalwidgets import PMToolBar, PMPushButtonPane, create_icon

properties = [
    {
        'name': 'button_new_script',
        'text': '新建\脚本',
        'icon_path': ':/pyqt/source/images/lc_newdoc.png'
    },
    {
        'name': 'button_open_script',
        'text': '打开\脚本',
        'icon_path': ':/pyqt/source/images/lc_open.png'
    },
    {'names': ['']}
]


class PMEditorToolbar(PMToolBar):
    def __init__(self):
        super().__init__()

        self.add_tool_button('button_new_script', '新建\n脚本',
                             create_icon(':/pyqt/source/images/lc_newdoc.png'))

        self.add_tool_button('button_open_script', '打开\n脚本',
                             create_icon(':/pyqt/source/images/lc_open.png'))

        self.add_buttons(3, ['button_search_for_file', 'button_clipboard', 'button_print'],
                         ['查找文件', '剪贴板', '打印'],
                         [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png",
                          ':/pyqt/source/images/lc_print.png'])
        self.addSeparator()

        self.add_buttons(3, ['button_search', 'button_replace', 'button_goto'], ['查找', '替换', '跳转到行'],
                         [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png",
                          ':/pyqt/source/images/lc_print.png'])
        self.get_control_widget('button_search').clicked.connect(lambda: print('查找！'))
        self.get_control_widget('button_replace').clicked.connect(lambda: print('替换！'))
        self.get_control_widget('button_goto').clicked.connect(lambda: print('跳转!'))

        self.add_buttons(2, ['button_comment', 'button_indent'], ['批量注释', '缩进'],
                         [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png"])
        self.add_buttons(2, ['button_uncomment', 'button_unindent'], ['取消注释', '减少缩进'],
                         [":/pyqt/source/images/lc_searchdialog.png", ":/pyqt/source/images/lc_pickthrough.png"])
        self.addSeparator()
        self.add_tool_button('button_run_script', '运行', create_icon(':/pyqt/source/images/run_exc.png'))
