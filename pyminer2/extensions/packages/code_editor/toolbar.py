from pmgwidgets.sourcemgr.iconutils import create_icon
from pmgwidgets.toolbars.toolbar import PMGToolBar

properties = [
    {
        'name': 'button_new_script',
        'text': '新建脚本',
        'icon_path': ':/color/source/theme/color/icons/script.svg'
    },
    {
        'name': 'button_open_script',
        'text': '打开脚本',
        'icon_path': ':/color/source/theme/color/icons/file.svg'
    },
    {'names': ['']}
]


class PMEditorToolbar(PMGToolBar):
    def __init__(self):
        super().__init__()

        self.add_tool_button('button_new_script', '新建脚本',
                             create_icon(':/color/source/theme/color/icons/script.svg'))

        self.add_tool_button('button_open_script', '打开脚本',
                             create_icon(':/color/source/theme/color/icons/file.svg'))

        self.add_buttons(3, ['button_search_for_file', 'button_clipboard', 'button_print'],
                         ['复制', '粘贴', '打印'],
                         [":/color/source/theme/color/icons/copy.svg", ":/color/source/theme/color/icons/paste.svg",
                          ':/color/source/theme/color/icons/print.svg'])
        self.get_control_widget('button_search_for_file').setEnabled(False)
        self.get_control_widget('button_clipboard').setEnabled(False)
        self.get_control_widget('button_print').setEnabled(False)
        self.addSeparator()

        self.add_buttons(2, ['button_search', 'button_goto'], ['查找/替换', '跳转到行'],
                         [":/color/source/theme/color/icons/find_replace.svg", ':/color/source/theme/color/icons/jump_line.svg'])

        self.get_control_widget('button_goto').setEnabled(False)

        self.add_buttons(2, ['button_comment', 'button_indent'], ['批量注释', '添加缩进'],
                         [":/color/source/theme/color/icons/annotation.svg",
                          ":/color/source/theme/color/icons/indent_right.svg"])
        self.add_buttons(2, ['button_uncomment', 'button_unindent'], ['取消注释', '减少缩进'],
                         [":/color/source/theme/color/icons/annotation_no.svg",
                          ":/color/source/theme/color/icons/indent_left.svg"])
        self.addSeparator()
        self.add_tool_button(
            'button_run_script',
            '运行',
            create_icon(':/color/source/theme/color/icons/run.svg'))

        self.add_tool_button('button_run_in_terminal',
                        '在终端运行',
                        create_icon(':/color/source/theme/color/icons/cmd.svg'))
