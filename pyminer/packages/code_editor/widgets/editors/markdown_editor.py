import re
import time

from PySide2.QtWidgets import QHBoxLayout, QMessageBox

from packages.qt_vditor.client import Window
from .base_editor import PMBaseEditor


class PMMarkdownEditor(PMBaseEditor):
    def __init__(self, parent=None):
        super(PMMarkdownEditor, self).__init__(parent=parent)
        # TODO 不应该直接引用qt_vditor，而是应该走interface
        self.textEdit = Window(url='http://127.0.0.1:5000/qt_vditor')
        self._path = ''
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.textEdit)

    def load_file(self, path: str):
        """加载文件"""
        self._path = path
        self.textEdit.load_file(path)

    def modified(self) -> bool:
        """
        获取当前文件是否被修改
        Returns:

        """
        return False

    def slot_save(self) -> None:
        self.textEdit.save_file()
        self.last_save_time = time.time()

    def get_code(self) -> str:
        with open(self._path, 'r', encoding='utf8') as f:
            text = f.read()
        code_blocks = re.findall('```python([\s\S]*?)```', text)
        if len(code_blocks) > 1:
            QMessageBox.warning(self, '未集成功能', '暂不支持运行含有两段及以上代码的Markdown文件！')
            return ''
        else:
            return code_blocks[0]
