# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 10:13
# @Author  : 别着急慢慢来
# @FileName: linestyles.py
# matplotlib中的常见颜色
from matplotlib.colors import LogNorm, NoNorm, BoundaryNorm, DivergingNorm, PowerNorm, SymLogNorm, TwoSlopeNorm, \
    Normalize

linestyles = ['-', '--', '-.', ':']
norms = ['Normalize', 'LogNorm', 'NoNorm']
markers = ['None', '.', 'o', 'v', '^', '<', '>', '1', '2', '3',
           '4', 's', 'p', '*', 'h', 'H', 'x', 'D', 'd', '|', '-']

arrowstyles = ['-', '->', '-[', '|-|', '-|>', '<-', '<->', '<|-', '<|-|>', 'fancy', 'simple', 'wedge']

grid_which = ['major', 'minor', 'both']

grid_axis = ['both', 'x', 'y']

locations = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',
             'center right', 'lower center', 'upper center', 'center']

draw_tabs = ['cover', 'new']

font_styles=['normal','italic','oblique']

font_weights=['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black']


def hex_to_rgb(hex):
    r = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    b = int(hex[5:7], 16)
    return r, g, b


def rgb_to_hex(r, g, b):
    color = "#"

    color += str(hex(r)).replace('x', '0')[-2:]

    color += str(hex(g)).replace('x', '0')[-2:]

    color += str(hex(b)).replace('x', '0')[-2:]

    return color.upper()


if __name__ == '__main__':
    # print(list(mpl_colors.keys())[list(mpl_colors.values()).index('#D8BFD8')])
    print(rgb_to_hex(10, 20, 30))
    # hex_to_rgb('#9ACD32')
