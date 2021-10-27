from typing import Dict

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont


class FontConfig:
    def __init__(self):
        """
        color是16位标准的。
        bold有以下几种选择。
        QFont::Thin	0	0
        QFont::ExtraLight	12	12
        QFont::Light	25	25
        QFont::Normal	50	50
        QFont::Medium	57	57
        QFont::DemiBold	63	63
        QFont::Bold	75	75
        QFont::ExtraBold	81	81
        QFont::Black
        """
        self.font_size = 15
        self.settings = {'normal': {'color': Qt.black, 'bold': QFont.Normal},
                         'keyword': {'color': Qt.darkBlue, 'bold': QFont.ExtraBold},
                         'builtin': {'color': Qt.darkRed, 'bold': QFont.Normal},
                         'constant': {'color': Qt.darkGreen, 'bold': QFont.Normal},
                         'decorator': {'color': Qt.darkBlue, 'bold': QFont.Normal},
                         'comment': {'color': Qt.darkGreen, 'bold': QFont.Normal},
                         'string': {'color': Qt.darkYellow, 'bold': QFont.Normal},
                         'number': {'color': Qt.darkMagenta, 'bold': QFont.Normal},
                         'error': {'color': Qt.darkRed, 'bold': QFont.Normal},
                         'pyqt': {'color': Qt.darkCyan, 'bold': QFont.Normal}
                         }
        # self.load_color_scheme(color_scheme_intellij)

    def load_color_scheme(self, scheme: Dict[str, str]):
        for name in scheme:
            assert name in self.settings.keys()
            self.set_font_color(name, scheme[name])

    def set_font_color(self, font_name: str, font_color: str):
        assert font_name in self.settings.keys()
        self.settings[font_name]['color'] = font_color

    def get_font_color(self, font_name: str):
        return self.settings[font_name]['color']

    def get_font_bold(self, font_name: str):
        return self.settings[font_name]['bold']

    def get_font_size(self) -> int:
        return self.font_size
