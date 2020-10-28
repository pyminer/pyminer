#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/10/4
@author: Irony
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: theme_xml_json
@description: 
"""

# import json
# import xmltodict
#
# xml = open('../themes/Material-Dark.xml', 'rb').read().decode()
# style = xmltodict.parse(xml, encoding='utf-8')
# print(json.dumps(style, indent=4))
#
# # 全局样式
# for s in style['NotepadPlus']['GlobalStyles']['WidgetStyle']:
#     name = s['@name']
#     fgColor = s['@fgColor']
#     bgColor = s['@bgColor']
#     print(name, fgColor, bgColor)

from lxml import etree

style = etree.parse('../themes/Material-Dark.xml')
# 全局样式
for c in style.xpath('/NotepadPlus/GlobalStyles/WidgetStyle'):
    print(c.get('name'), c.get('fgColor'), c.get('bgColor'))

# 关键词高亮
for w in style.xpath('/NotepadPlus/LexerStyles/LexerType[@name="python"]/WordsStyle'):
    print(w.get('name'), w.get('fgColor'), w.get('bgColor'))
