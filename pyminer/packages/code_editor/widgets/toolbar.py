from widgets import create_icon, PMGToolBar, QComboBox
from ..utils.base_object import CodeEditorBaseObject


class PMEditorToolbar(CodeEditorBaseObject, PMGToolBar):

    def __init__(self):
        super(PMEditorToolbar, self).__init__()

        self.add_tool_button('button_new_script', self.tr('New Script'), self.tr('New Script'),
                             create_icon(':/resources/icons/script.svg'))

        self.add_tool_button(
            'button_open_script', self.tr('Open Script'), self.tr('Open Script'),
            create_icon(':/resources/icons/open.svg'))

        self.add_tool_button('button_save', self.tr('Save'), self.tr('Save'),
                             create_icon(":/resources/icons/save.svg"))
        self.addSeparator()
        self.add_tool_button(
            'button_search', self.tr('Find'), self.tr('Find'),
            create_icon(":/resources/icons/find_replace.svg"))

        self.add_buttons(2, ['button_comment', 'button_goto'], [self.tr('Toggle Comment'), self.tr('Goto Line')],
                         [":/resources/icons/annotation.svg",
                          ':/resources/icons/jump_line.svg'])

        self.get_control_widget('button_goto').setEnabled(True)

        self.add_buttons(2, ['button_indent', 'button_unindent'], [self.tr('Indent'), self.tr('Dedent')],
                         [":/resources/icons/indent_left.svg",
                          ":/resources/icons/indent_right.svg"])
        self.addSeparator()
        self.add_tool_button('button_run_script', self.tr('IPython'), self.tr('IPython'),
                             create_icon(':/resources/icons/run.svg'))

        self.add_tool_button('button_run_isolated', self.tr('Separately'), self.tr('Separately'),
                             create_icon(':/resources/icons/cmd.svg'))
        self.add_tool_button('button_run_in_terminal', self.tr('Terminal'), self.tr('Terminal'),
                             create_icon(':/resources/icons/cmd.svg'))
        # self.add_tool_button('button_instant_boot', self.tr('Instant Boot'),
        #                      self.tr('Start your program instantly with modules preloaded.'),
        #                      create_icon(os.path.join(os.path.dirname(__file__), 'source', 'lightening.png')))

        self.add_tool_button('button_instant_boot', self.tr('Instant Boot'),
                             self.tr('Run script with common module preloaded to shorten interpterter startup-time.'),
                             create_icon(str(self.settings.icons_dir / 'lightening.png')))
        # self.add_tool_button('button_debug', self.tr('Debug'),
        #                      create_icon(':/resources/icons/debug.svg'))
        interpreter_sel_widget = self.add_widget('combobox_interpreter', QComboBox())
        interpreter_sel_widget.setMinimumWidth(200)

    def get_toolbar_text(self) -> str:
        return self.tr('Editor')

    def insert_after(self) -> str:
        return 'toolbar_home'
