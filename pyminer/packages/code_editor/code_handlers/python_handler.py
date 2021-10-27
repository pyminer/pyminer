import logging

from yapf.yapflib import yapf_api

from packages.code_editor.code_handlers.base_handler import BaseHandler

logger = logging.getLogger(__name__)


class PythonHandler(BaseHandler):
    def run_code(self, code: str, hint: str = ''):
        if hint == '':
            hint = self.tr('Run code')
        self.interfaces.ipython_console.run_command(command=code, hint_text=hint, hidden=False)

    def run_selected_code(self):
        code = self.analyzer.selected_code
        self.interfaces.ipython_console.run_command(command=code, hint_text=code, hidden=False)

    def format_code(self):
        try:
            code, _ = yapf_api.FormatCode(
                self.analyzer.code, style_config=str(self.settings.assets_dir / '.style.yapf'))
        except Exception as e:
            logger.exception(e)
            code = self.analyzer.code
        return self.analyzer_class(code, self.analyzer.cursor, self.analyzer.selection_range)
