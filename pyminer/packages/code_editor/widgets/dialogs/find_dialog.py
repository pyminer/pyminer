from typing import Callable, TYPE_CHECKING

from PySide2.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout

from widgets import PMGPanel

if TYPE_CHECKING:
    from ...widgets.text_edit.base_text_edit import PMBaseCodeEdit
    from ..editors.base_editor import PMBaseEditor


class PMFindDialog(QDialog):
    tr: Callable[[str], str]

    def __init__(self, parent: 'PMBaseEditor' = None):
        super(PMFindDialog, self).__init__(parent)
        self.text_editor = parent
        self.text_edit: 'PMBaseCodeEdit' = parent.text_edit
        views = [
            ('line_ctrl', 'text_to_find', self.tr('Text to Find'), ''),
            ('line_ctrl', 'text_to_replace', self.tr('Text to Replace'), ''),
            ('check_ctrl', 'wrap', self.tr('Wrap'), True),
            ('check_ctrl', 'regex', self.tr('Regex'), False),
            ('check_ctrl', 'case_sensitive', self.tr('Case Sensitive'), True),
            ('check_ctrl', 'whole_word', self.tr('Whole Word'), True),
        ]
        self.settings_panel = PMGPanel(parent=self, views=views)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.settings_panel)
        self.button_up = QPushButton(self.tr('Up'))
        self.button_down = QPushButton(self.tr('Down'))
        self.button_replace = QPushButton(self.tr('Replace'))
        self.button_replace_all = QPushButton(self.tr('Replace All'))

        self.button_up.clicked.connect(self.search_up)
        self.button_down.clicked.connect(self.search_down)
        self.button_replace.clicked.connect(self.replace_current)
        self.button_replace_all.clicked.connect(self.replace_all)

        self.button_bar = QHBoxLayout()
        self.button_bar.addWidget(self.button_up)
        self.button_bar.addWidget(self.button_down)
        self.button_bar.addWidget(self.button_replace)
        self.button_bar.addWidget(self.button_replace_all)
        self.button_bar.setContentsMargins(0, 0, 0, 0)
        self.layout().addLayout(self.button_bar)

    def search_up(self):
        settings = self.settings_panel.get_value()
        self.text_editor.search_word(forward=True, **settings)

        pass

    def search_down(self):
        """
        反方向查找。注意，简单的设置qsci的forward=False是不够的，还需要对位置进行处理。
        这似乎是QSciScintilla的bug.
        """
        settings = self.settings_panel.get_value()
        self.text_editor.search_word(forward=False, **settings)

        pass

    def replace_current(self):
        text: str = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        if self.text_edit.is_text_selected:
            self.text_edit.replace_selection(text)
            self.search_up()

    def replace_all(self):
        settings = self.settings_panel.get_value()
        text_to_replace = self.settings_panel.widgets_dic['text_to_replace'].get_value()
        while 1:
            b = self.text_editor.search_word(forward=True, **settings)
            if b:
                self.text_edit.replace_selection(text_to_replace)

            else:
                break

    def show(self) -> None:
        super().show()
        if self.text_edit.selected_code != '':
            self.settings_panel.set_value({'text_to_find': self.text_edit.selected_code})

    def show_replace_actions(self, replace_on: bool = False):
        self.settings_panel.get_ctrl('text_to_replace').setVisible(replace_on)
        self.button_replace.setVisible(replace_on)
        self.button_replace_all.setVisible(replace_on)

    def closeEvent(self, a0: 'QCloseEvent') -> None:
        pass
        # sel = self.text_edit.getCursorPosition()
        # self.text_edit.setSelection(sel[0], sel[1], sel[0], sel[1])

    def close(self) -> bool:
        return False
