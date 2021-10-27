from typing import Union


class PMGPlotCustomizer():
    def __init__(self):
        self._line_color = '#000000'
        self._line_style = '--'
        self._line_width = 2
        self._border_color = '#000000'
        self._border_width = 2
        self._symbol = 't'
        self._item_color = '#000000'
        self._face_color = '#ffffff'
        self._legend_face_color = '#ffffff'
        self._symbols_dic = {}

    @property
    def border_color(self):
        return self._border_color

    @border_color.setter
    def border_color(self, color: str):
        self._border_color = color

    @property
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, border_width: Union[int, float]):
        self._border_width = border_width

    @property
    def face_color(self):
        return self._face_color

    @face_color.setter
    def face_color(self, color: str):
        self._face_color = color

    @property
    def item_color(self):
        return self._item_color

    @item_color.setter
    def item_color(self, color: str):
        self._item_color = color

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, color: str):
        self._line_color = color

    @property
    def line_style(self):
        return self._line_style

    @line_style.setter
    def line_style(self, style: str):
        self._line_style = style

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, width: Union[int, float]):
        assert isinstance(width, (int, float))
        self._line_width = width

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str):
        if symbol in self._symbols_dic.keys():
            self._symbol = self._symbols_dic[symbol]
        else:
            raise ValueError(
                'Symbol \'%s\' is not allowed.\nAll allowed symbols are:%s' % (symbol,
                                                                               list(self._symbols_dic.keys())))

    @property
    def legend_face_color(self):
        return self._legend_face_color

    @legend_face_color.setter
    def legend_face_color(self, color):
        self._legend_face_color = color
