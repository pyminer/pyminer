import logging
from typing import List

from PySide2.QtCore import QPoint
from jedi.api.classes import Completion as CompletionResult

from .base_text_edit import PMBaseCodeEdit
from ...code_handlers.python_handler import PythonHandler
from ...utils.auto_complete_thread.python_auto_complete import PythonAutoCompleteThread
from ...utils.highlighter.python_highlighter import PythonHighlighter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PMPythonCodeEdit(PMBaseCodeEdit):
    last_mouse_position: QPoint

    auto_complete_thread_class = PythonAutoCompleteThread
    highlighter_class = PythonHighlighter
    handler_class = PythonHandler

    def on_autocomp_signal_received(self, text_cursor_content: tuple, completions: List[CompletionResult]):
        """
        当收到自动补全提示信号时，执行的函数。
        :param text_cursor_content: (row,col,hint_when_completion_triggered)
        :param completions:
        :return:
        """

        hint = self._get_hint()
        if hint.startswith(text_cursor_content[2]):
            if len(completions) == 1:
                if completions[0].name == self._get_hint():
                    self.hide_autocomp()
                    return
            self.autocomp_show(completions)
        else:
            self.hide_autocomp()
