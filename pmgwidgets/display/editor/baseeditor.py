import sys

from PyQt5.Qsci import QsciScintilla, QsciLexerSQL, QsciLexer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QStyleFactory


class PMBaseEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Source Code Pro', 12))  # Consolas

    def set_lexer(self, lexer:'QsciLexer'):
        self._lexer = lexer
        self._lexer.setFont(self.font())
        self.setLexer(self._lexer)

    # def _init_lexer(self) -> None:
    #     """
    #     初始化语法解析器
    #
    #     :return: None
    #     """
    #     self._lexer = QsciLexerSQL(self)
    #     # self._lexer.setFont(self.font())
    #     self.setLexer(self._lexer)


if __name__ == '__main__':
    from pmgwidgets.display.editor.lexers.cythonlexer import CythonLexer
    app = QApplication(sys.argv)
    textedit = PMBaseEditor()
    textedit.setLexer(CythonLexer(textedit))
    initial_text = """
cdef public struct Vehicle:
    int speed
    float power

cdef api void activate(Vehicle *v):
    if v.speed >= 88 and v.power >= 1.21:
        print("Time travel achieved")
    """
    textedit.setText(initial_text)
    textedit.show()
    app.exec_()