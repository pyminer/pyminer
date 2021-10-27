"""
a parser like css/qss
names-property:value
支持使用汉语拼音缩写的形式来输入简称。括号里面就是别名
names:
    line(xt/线条)
    item(tx/图形)
    canvas(hb/画布)
    legend(tl/图例)
    axis(zbz/坐标轴)

properties:
    width(w/kd/宽度)
    height(h/gd/高度)
    size(dx/大小)

    color(c/ys/颜色)

    textcolor(wzys/文字颜色)
    fillcolor(tcys/fc/填充颜色)
    bordercolor(byys/边缘颜色)

    shape(xz/形状)
    fontsize(zh/字号)

    transparency(tmd/透明度)

"""
d = {  # standard dict!
    'line_color': '#ff0000', 'line_shape': '--', 'line_width': 10,

    'item_size': 8, 'item_textcolor': '#000000', 'item_fillcolor': '#00ff00', 'item_border_color': '#0000ff',
    'item_transparency': 100, 'item_shape': 'x',

    'legend_textcolor': '#000000', 'legend_fillcolor': '#ffffff', 'legend_border_color': '#0000ff',
    'legend_transparency': 100,

    'canvas_color': '#ffffff',
    'axis_textcolor': '#000000', 'axis_fontsize': 10
}
mapping = {
    'width': 'width', 'height': 'height', 'size': 'size', 'color': 'color', 'textcolor': 'textcolor',
    'fillcolor': 'fillcolor',
    'bordercolor': 'bordercolor', 'shape': 'shape', 'fontsize': 'fontsize', 'transparency': 'transparency',
    'line': 'line', 'item': 'item', 'canvas': 'canvas', 'legend': 'legend', 'axis': 'axis',

    'kd': 'width', 'gd': 'height', 'dx': 'size', 'ys': 'color', 'wzys': 'textcolor', 'tcys': 'fillcolor',
    'byys': 'bordercolor', 'xz': 'shape', 'zh': 'fontsize', 'tmd': 'transparency',
    'xt': 'line', 'tx': 'item', 'hb': 'canvas', 'tl': 'legend', 'zbz': 'axis'
}


def parse(sym: str):
    """
    parser for drawing syntax
    """
    if sym.find('_') != -1:
        l = sym.split('_')
        # print(l)
        mapped = []
        for s in l:
            assert s.strip() in mapping.keys()
            mapped.append(mapping[s.strip()])
        res = '_'.join(mapped)
    else:
        mapped = []
        loops = 0
        while (1):
            loops += 1
            if len(sym.strip()) > 0:
                for k in mapping.keys():
                    if sym.startswith(k):
                        mapped.append(mapping[k])
                        sym = sym[len(k):]
                        break
            else:
                break
            if loops > 10:
                raise ValueError('too many loops,expr \'%s\' maybe too long' % sym)

        res = '_'.join(mapped)
    print(res)
    assert res in d.keys(), 'res %s not in dict.keys()' % res
    return res


if __name__ == '__main__':
    parse('xt_kd')  # 线条宽度
    parse('xtkd')  # 线条宽度（汉语拼音缩写）
    parse('txxz')  # 图形形状（汉语拼音缩写）
