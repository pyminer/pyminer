from PySide2.QtGui import QSyntaxHighlighter, QColor


class BaseHighlighter(QSyntaxHighlighter):
    ERROR = 1
    WARNING = 2
    HINT = 3
    DEHIGHLIGHT = 4

    HIGHLIGHT_COLOR = {ERROR: QColor(255, 65, 65, 200), WARNING: QColor(255, 255, 65, 100),
                       HINT: QColor(155, 155, 155, 100), DEHIGHLIGHT: QColor(155, 155, 155, 100)}
