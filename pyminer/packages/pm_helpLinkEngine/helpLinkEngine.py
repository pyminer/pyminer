# -*- encoding: utf-8 -*-
"""
    说明：由于之前帮助按钮模式做的效果不是很理想，目前计划是做一个新的模块作为临时结局方案
"""
import webbrowser

class helpLinkEngine(object):
    def __init__(self):
        self.url_dict = {
            "dataio_sample_showhelp":'导入其他数据分析软件的工作表?sort_id=3265627'
        }

    def openHelp(self, tag = ""):
        if tag in self.url_dict:
            url = "https://gitee.com/py2cn/pyminer/wikis/" + self.url_dict[tag]
            webbrowser.open(url)
        else:
            from PySide2.QtWidgets import QMessageBox
            QMessageBox.warning(None, '警告', '当前模块暂无帮助文档！', QMessageBox.Ok)

helpLink = helpLinkEngine()
