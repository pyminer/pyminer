# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pmagg_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(614, 449)
        icon = QIcon()
        icon.addFile(u"../icons/Icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionX_X = QAction(MainWindow)
        self.actionX_X.setObjectName(u"actionX_X")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.action_load_figure = QAction(MainWindow)
        self.action_load_figure.setObjectName(u"action_load_figure")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.action_save_image = QAction(MainWindow)
        self.action_save_image.setObjectName(u"action_save_image")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.action_save_figure = QAction(MainWindow)
        self.action_save_figure.setObjectName(u"action_save_figure")
        self.action_export_settings = QAction(MainWindow)
        self.action_export_settings.setObjectName(u"action_export_settings")
        self.action_import_settings = QAction(MainWindow)
        self.action_import_settings.setObjectName(u"action_import_settings")
        self.action_print = QAction(MainWindow)
        self.action_print.setObjectName(u"action_print")
        self.actionscience = QAction(MainWindow)
        self.actionscience.setObjectName(u"actionscience")
        self.actionieee = QAction(MainWindow)
        self.actionieee.setObjectName(u"actionieee")
        self.action_text = QAction(MainWindow)
        self.action_text.setObjectName(u"action_text")
        self.action_text.setCheckable(True)
        self.action_annotation = QAction(MainWindow)
        self.action_annotation.setObjectName(u"action_annotation")
        self.action_annotation.setCheckable(True)
        self.action_rectangle = QAction(MainWindow)
        self.action_rectangle.setObjectName(u"action_rectangle")
        self.action_rectangle.setCheckable(True)
        self.action_oval = QAction(MainWindow)
        self.action_oval.setObjectName(u"action_oval")
        self.action_oval.setCheckable(True)
        self.action_arrow = QAction(MainWindow)
        self.action_arrow.setObjectName(u"action_arrow")
        self.action_arrow.setCheckable(True)
        self.action_main_view = QAction(MainWindow)
        self.action_main_view.setObjectName(u"action_main_view")
        self.action_left_view = QAction(MainWindow)
        self.action_left_view.setObjectName(u"action_left_view")
        self.action_right_view = QAction(MainWindow)
        self.action_right_view.setObjectName(u"action_right_view")
        self.action_bottom_view = QAction(MainWindow)
        self.action_bottom_view.setObjectName(u"action_bottom_view")
        self.action_top_view = QAction(MainWindow)
        self.action_top_view.setObjectName(u"action_top_view")
        self.action_back_view = QAction(MainWindow)
        self.action_back_view.setObjectName(u"action_back_view")
        self.action45_45_view = QAction(MainWindow)
        self.action45_45_view.setObjectName(u"action45_45_view")
        self.action45_m45_view = QAction(MainWindow)
        self.action45_m45_view.setObjectName(u"action45_m45_view")
        self.action_m45_45_view = QAction(MainWindow)
        self.action_m45_45_view.setObjectName(u"action_m45_45_view")
        self.action_m45_m45_view = QAction(MainWindow)
        self.action_m45_m45_view.setObjectName(u"action_m45_m45_view")
        self.action_arbitrary_view = QAction(MainWindow)
        self.action_arbitrary_view.setObjectName(u"action_arbitrary_view")
        self.action_close = QAction(MainWindow)
        self.action_close.setObjectName(u"action_close")
        self.action_axis = QAction(MainWindow)
        self.action_axis.setObjectName(u"action_axis")
        self.action_zh_cn = QAction(MainWindow)
        self.action_zh_cn.setObjectName(u"action_zh_cn")
        self.action_zh_cn.setCheckable(False)
        self.action_zh_cn.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.action_zh_cn.setIconVisibleInMenu(True)
        self.action_english = QAction(MainWindow)
        self.action_english.setObjectName(u"action_english")
        self.action_copy_figure_to_clipboard = QAction(MainWindow)
        self.action_copy_figure_to_clipboard.setObjectName(u"action_copy_figure_to_clipboard")
        self.action_legend_draggable = QAction(MainWindow)
        self.action_legend_draggable.setObjectName(u"action_legend_draggable")
        self.action_move_text = QAction(MainWindow)
        self.action_move_text.setObjectName(u"action_move_text")
        self.action_move_text.setCheckable(True)
        self.action_move_annotation = QAction(MainWindow)
        self.action_move_annotation.setObjectName(u"action_move_annotation")
        self.action_move_annotation.setCheckable(True)
        self.action_move_rectangle = QAction(MainWindow)
        self.action_move_rectangle.setObjectName(u"action_move_rectangle")
        self.action_move_rectangle.setCheckable(True)
        self.action_move_oval = QAction(MainWindow)
        self.action_move_oval.setObjectName(u"action_move_oval")
        self.action_move_oval.setCheckable(True)
        self.action_move_arrow = QAction(MainWindow)
        self.action_move_arrow.setObjectName(u"action_move_arrow")
        self.action_move_arrow.setCheckable(True)
        self.action_axis_edit = QAction(MainWindow)
        self.action_axis_edit.setObjectName(u"action_axis_edit")
        self.action_title_edit = QAction(MainWindow)
        self.action_title_edit.setObjectName(u"action_title_edit")
        self.action_legend_edit = QAction(MainWindow)
        self.action_legend_edit.setObjectName(u"action_legend_edit")
        self.action_grid_edit = QAction(MainWindow)
        self.action_grid_edit.setObjectName(u"action_grid_edit")
        self.action_show_toolbar = QAction(MainWindow)
        self.action_show_toolbar.setObjectName(u"action_show_toolbar")
        self.action_help = QAction(MainWindow)
        self.action_help.setObjectName(u"action_help")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_show_menubar = QAction(MainWindow)
        self.action_show_menubar.setObjectName(u"action_show_menubar")
        self.action_tab = QAction(MainWindow)
        self.action_tab.setObjectName(u"action_tab")
        self.action_line = QAction(MainWindow)
        self.action_line.setObjectName(u"action_line")
        self.action_line.setCheckable(True)
        self.action_matplotlib = QAction(MainWindow)
        self.action_matplotlib.setObjectName(u"action_matplotlib")
        self.action_polygon = QAction(MainWindow)
        self.action_polygon.setObjectName(u"action_polygon")
        self.action_polygon.setCheckable(True)
        self.action_image = QAction(MainWindow)
        self.action_image.setObjectName(u"action_image")
        self.action_image.setCheckable(True)
        self.action_5 = QAction(MainWindow)
        self.action_5.setObjectName(u"action_5")
        self.action_default_setting = QAction(MainWindow)
        self.action_default_setting.setObjectName(u"action_default_setting")
        self.action_color_table = QAction(MainWindow)
        self.action_color_table.setObjectName(u"action_color_table")
        self.action_code = QAction(MainWindow)
        self.action_code.setObjectName(u"action_code")
        self.action_space = QAction(MainWindow)
        self.action_space.setObjectName(u"action_space")
        self.action_home = QAction(MainWindow)
        self.action_home.setObjectName(u"action_home")
        self.action_home.setCheckable(False)
        self.action_front = QAction(MainWindow)
        self.action_front.setObjectName(u"action_front")
        self.action_front.setCheckable(False)
        self.action_back = QAction(MainWindow)
        self.action_back.setObjectName(u"action_back")
        self.action_back.setCheckable(False)
        self.action_zoom = QAction(MainWindow)
        self.action_zoom.setObjectName(u"action_zoom")
        self.action_zoom.setCheckable(True)
        self.action_pan = QAction(MainWindow)
        self.action_pan.setObjectName(u"action_pan")
        self.action_pan.setCheckable(True)
        self.action_rotate = QAction(MainWindow)
        self.action_rotate.setObjectName(u"action_rotate")
        self.action_rotate.setCheckable(True)
        self.action_legend = QAction(MainWindow)
        self.action_legend.setObjectName(u"action_legend")
        self.action_colorbar = QAction(MainWindow)
        self.action_colorbar.setObjectName(u"action_colorbar")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 614, 23))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setStyleSheet(u"")
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menuBar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_annotation = QMenu(self.menuBar)
        self.menu_annotation.setObjectName(u"menu_annotation")
        self.menu_annotation.setStyleSheet(u"")
        self.menu_6 = QMenu(self.menuBar)
        self.menu_6.setObjectName(u"menu_6")
        self.menu_6.setStyleSheet(u"")
        self.menu_edit = QMenu(self.menuBar)
        self.menu_edit.setObjectName(u"menu_edit")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMinimumSize(QSize(0, 0))
        self.toolBar.setMaximumSize(QSize(16777215, 22))
        self.toolBar.setStyleSheet(u"")
        self.toolBar.setMovable(False)
        self.toolBar.setOrientation(Qt.Horizontal)
        self.toolBar.setIconSize(QSize(30, 30))
        self.toolBar.setFloatable(True)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menu_edit.menuAction())
        self.menuBar.addAction(self.menu_annotation.menuAction())
        self.menuBar.addAction(self.menu_6.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.menuFile.addAction(self.action_load_figure)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_save_figure)
        self.menuFile.addAction(self.action_save_image)
        self.menuFile.addAction(self.action_close)
        self.menu_2.addAction(self.action_help)
        self.menu_2.addAction(self.action_color_table)
        self.menu_2.addAction(self.action_matplotlib)
        self.menu_annotation.addAction(self.action_text)
        self.menu_annotation.addAction(self.action_annotation)
        self.menu_annotation.addAction(self.action_rectangle)
        self.menu_annotation.addAction(self.action_oval)
        self.menu_annotation.addAction(self.action_arrow)
        self.menu_annotation.addAction(self.action_image)
        self.menu_6.addAction(self.action_main_view)
        self.menu_6.addAction(self.action_left_view)
        self.menu_6.addAction(self.action_right_view)
        self.menu_6.addAction(self.action_bottom_view)
        self.menu_6.addAction(self.action_top_view)
        self.menu_6.addAction(self.action_back_view)
        self.menu_6.addAction(self.action45_45_view)
        self.menu_6.addAction(self.action45_m45_view)
        self.menu_6.addAction(self.action_m45_45_view)
        self.menu_6.addAction(self.action_m45_m45_view)
        self.menu_6.addAction(self.action_arbitrary_view)
        self.menu_6.addSeparator()
        self.menu_6.addAction(self.action_show_toolbar)
        self.menu_6.addAction(self.action_show_menubar)
        self.menu_6.addAction(self.action_zoom)
        self.menu_6.addAction(self.action_pan)
        self.menu_6.addAction(self.action_rotate)
        self.menu_edit.addAction(self.action_default_setting)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_copy_figure_to_clipboard)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_axis_edit)
        self.menu_edit.addAction(self.action_space)
        self.menu_edit.addAction(self.action_title_edit)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_home)
        self.menu_edit.addAction(self.action_back)
        self.menu_edit.addAction(self.action_front)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.action_legend)
        self.menu_edit.addAction(self.action_colorbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7ed8\u56fe", None))
        self.actionX_X.setText(QCoreApplication.translate("MainWindow", u"X \u6807\u7b7e(X)", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.action_load_figure.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165figure\u5bf9\u8c61", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.action_save_image.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u56fe\u7247", None))
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u4e3afigure\u5bf9\u8c61", None))
        self.action_save_figure.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58figure\u5bf9\u8c61", None))
        self.action_export_settings.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u914d\u7f6e\u6587\u4ef6", None))
        self.action_import_settings.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u914d\u7f6e\u6587\u4ef6", None))
        self.action_print.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5370", None))
        self.actionscience.setText(QCoreApplication.translate("MainWindow", u"science", None))
        self.actionieee.setText(QCoreApplication.translate("MainWindow", u"ieee", None))
        self.action_text.setText(QCoreApplication.translate("MainWindow", u"\u6587\u5b57", None))
        self.action_annotation.setText(QCoreApplication.translate("MainWindow", u"\u5750\u6807", None))
        self.action_rectangle.setText(QCoreApplication.translate("MainWindow", u"\u77e9\u5f62", None))
        self.action_oval.setText(QCoreApplication.translate("MainWindow", u"\u692d\u5706", None))
        self.action_arrow.setText(QCoreApplication.translate("MainWindow", u"\u7bad\u5934", None))
        self.action_main_view.setText(QCoreApplication.translate("MainWindow", u"\u6b63\u89c6\u56fe", None))
        self.action_left_view.setText(QCoreApplication.translate("MainWindow", u"\u5de6\u89c6\u56fe", None))
        self.action_right_view.setText(QCoreApplication.translate("MainWindow", u"\u53f3\u89c6\u56fe", None))
        self.action_bottom_view.setText(QCoreApplication.translate("MainWindow", u"\u4fef\u89c6\u56fe", None))
        self.action_top_view.setText(QCoreApplication.translate("MainWindow", u"\u4ef0\u89c6\u56fe", None))
        self.action_back_view.setText(QCoreApplication.translate("MainWindow", u"\u80cc\u89c6\u56fe ", None))
        self.action45_45_view.setText(QCoreApplication.translate("MainWindow", u"45\u00b0/45\u00b0\u4fa7\u89c6\u56fe", None))
        self.action45_m45_view.setText(QCoreApplication.translate("MainWindow", u"45\u00b0/-45\u00b0\u4fa7\u89c6\u56fe", None))
        self.action_m45_45_view.setText(QCoreApplication.translate("MainWindow", u"-45\u00b0/45\u00b0\u4fa7\u89c6\u56fe", None))
        self.action_m45_m45_view.setText(QCoreApplication.translate("MainWindow", u"-45\u00b0/-45\u00b0\u4fa7\u89c6\u56fe", None))
        self.action_arbitrary_view.setText(QCoreApplication.translate("MainWindow", u"\u4efb\u610f\u89c6\u56fe", None))
        self.action_close.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.action_axis.setText(QCoreApplication.translate("MainWindow", u"\u5750\u6807\u8f74", None))
        self.action_zh_cn.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u6587", None))
        self.action_zh_cn.setIconText(QCoreApplication.translate("MainWindow", u"\u4e2d\u6587", None))
        self.action_english.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.action_copy_figure_to_clipboard.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236\u5230\u526a\u8d34\u677f", None))
        self.action_legend_draggable.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u4f8b\u53ef\u62d6\u62fd", None))
        self.action_move_text.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8\u6587\u5b57", None))
        self.action_move_annotation.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8\u5750\u6807", None))
        self.action_move_rectangle.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8\u77e9\u5f62", None))
        self.action_move_oval.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8\u692d\u5706", None))
        self.action_move_arrow.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8\u7bad\u5934", None))
        self.action_axis_edit.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u6574\u5750\u6807\u8f74", None))
        self.action_title_edit.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u6807\u9898", None))
        self.action_legend_edit.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u56fe\u4f8b", None))
        self.action_grid_edit.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u7f51\u683c", None))
        self.action_show_toolbar.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a/\u9690\u85cf\u5de5\u5177\u680f", None))
        self.action_help.setText(QCoreApplication.translate("MainWindow", u"\u5728\u7ebf\u6587\u6863", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u7981\u7528\u53f3\u952e\u529f\u80fd", None))
        self.action_show_menubar.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a/\u9690\u85cf\u83dc\u5355\u680f", None))
        self.action_tab.setText(QCoreApplication.translate("MainWindow", u"\u9690\u85cftab\u9875", None))
        self.action_line.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u7ebf", None))
        self.action_matplotlib.setText(QCoreApplication.translate("MainWindow", u"matplotlib\u5b98\u7f51", None))
        self.action_polygon.setText(QCoreApplication.translate("MainWindow", u"\u591a\u8fb9\u5f62", None))
        self.action_image.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None))
        self.action_5.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0/\u79fb\u52a8\u5706", None))
        self.action_default_setting.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u6539\u9ed8\u8ba4\u8bbe\u7f6e", None))
        self.action_color_table.setText(QCoreApplication.translate("MainWindow", u"\u5e38\u7528\u8272\u5f69\u8868", None))
        self.action_code.setText(QCoreApplication.translate("MainWindow", u"\u793a\u4f8b\u4ee3\u7801", None))
        self.action_space.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u6574\u95f4\u9694", None))
        self.action_home.setText(QCoreApplication.translate("MainWindow", u"\u56de\u5230\u6700\u521d", None))
        self.action_front.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d", None))
        self.action_back.setText(QCoreApplication.translate("MainWindow", u"\u64a4\u9500", None))
        self.action_zoom.setText(QCoreApplication.translate("MainWindow", u"\u7f29\u653e", None))
        self.action_pan.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8", None))
        self.action_rotate.setText(QCoreApplication.translate("MainWindow", u"\u65cb\u8f6c", None))
        self.action_legend.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a/\u9690\u85cf\u56fe\u4f8b", None))
        self.action_colorbar.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u989c\u8272\u6761", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u5b50\u56fe", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.menu_annotation.setTitle(QCoreApplication.translate("MainWindow", u"\u6ce8\u91ca", None))
        self.menu_6.setTitle(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

