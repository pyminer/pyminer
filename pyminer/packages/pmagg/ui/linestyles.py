# -*- coding: utf-8 -*-
# @Time    : 2020/9/9 10:13
# @Author  : 别着急慢慢来
# @FileName: linestyles.py
# matplotlib中的常见颜色
from matplotlib.colors import LogNorm, NoNorm, BoundaryNorm, PowerNorm, SymLogNorm, TwoSlopeNorm, \
    Normalize

languages = ['en', 'zh_CN']

linestyles = ['-', '--', '-.', ':']
norms = ['Normalize', 'LogNorm', 'NoNorm']
markers = ['None', '.', 'o', 'v', '^', '<', '>', '1', '2', '3',
           '4', 's', 'p', '*', 'h', 'H', 'x', 'D', 'd', '|', '-']

arrowstyles = ['-', '->', '-[', '|-|', '-|>', '<-', '<->', '<|-', '<|-|>', 'fancy', 'simple', 'wedge']

connection_styles=["angle3,angleA=90,angleB=0",
                   "angle3,angleA=0,angleB=90",
                   "arc3,rad=0.",
                   "arc3,rad=0.3",
                   "arc3,rad=-0.3",
                   "angle,angleA=-90,angleB=180,rad=0",
                   "angle,angleA=-90,angleB=180,rad=5",
                   "angle,angleA=-90,angleB=10,rad=5",
                   "arc,angleA=-90,angleB=0,armA=30,armB=30,rad=0",
                   "arc,angleA=-90,angleB=0,armA=30,armB=30,rad=5",
                   "arc,angleA=-90,angleB=0,armA=0,armB=40,rad=0",
                   "bar,fraction=0.3",
                   "bar,fraction=-0.3",
                   "bar,angle=180,fraction=-0.2"]

grid_which = ['major', 'minor', 'both']

grid_axis = ['both', 'x', 'y']

locations = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',
             'center right', 'lower center', 'upper center', 'center']

draw_tabs = ['cover', 'new']

font_styles = ['normal', 'italic', 'oblique']

font_weights = ['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi',
                'bold', 'heavy', 'extra bold', 'black']

box_styles = ['None', 'circle', 'darrow', 'larrow', 'rarrow', 'round', 'round4', 'roundtooth', 'sawtooth', 'square']


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
