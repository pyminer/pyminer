import os
import webbrowser

# 也就是widget_right
from PyQt5.QtWidgets import QWidget, QGridLayout, QSpacerItem, QSizePolicy, QMainWindow, QListWidget, QListWidgetItem, \
    QHBoxLayout, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMenu, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QCursor, QResizeEvent
from PyQt5.QtCore import Qt, QCoreApplication, QSize

from pyminer2.pmutil import get_root_dir
from pyminer2.extensions.extensions_manager.manager import extensions_manager
from pyminer2.ui.generalwidgets import PMToolButton, PMFlowLayoutWithGrid


class ControlPanel:
    pass


class PMPageData(QWidget):
    flow_layout: 'PMFlowLayoutWithGrid' = None

    def __init__(self):
        super().__init__()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self.flow_layout is not None:
            self.flow_layout.on_resize()

    def setup_ui(self):
        # self.setMaximumHeight(300)
        from .resources import icon_lc_connectorcurve, icon_transition_random, icon_formfilternavigator, \
            icon_data_provider, icon_lc_togglemergecells, icon_lc_datadatapilotrun, icon_delete_columns, \
            icon_mergedocuments, icon_lc_accepttrackedchange, \
            icon_lc_datasubtotals, icon_dbdistinctvalues, icon_entirecolumn, icon_lc_selectdb, \
            icon_lc_dbviewtablenames, icon_lc_dataarearefresh, icon_NavOverFlow_Info, \
            icon_graphicfilterpopart, icon_deleterows, icon_lc_renametable, icon_lc_formatcolumns

        self.flow_layout = PMFlowLayoutWithGrid(self)
        self.btn_data_filter = PMToolButton()
        self.btn_data_filter.setMinimumSize(QSize(80, 60))
        self.btn_data_filter.setMaximumSize(QSize(80, 60))

        self.btn_data_filter.setIcon(icon_lc_connectorcurve)
        self.btn_data_filter.setIconSize(QSize(32, 32))
        self.btn_data_filter.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_filter.setObjectName("btn_data_filter")
        self.flow_layout.addWidget(self.btn_data_filter, 5, 4, 1, 1)
        self.btn_data_sample = PMToolButton()
        self.btn_data_sample.setMinimumSize(QSize(80, 60))
        self.btn_data_sample.setMaximumSize(QSize(80, 60))

        self.btn_data_sample.setIcon(icon_transition_random)
        self.btn_data_sample.setIconSize(QSize(32, 32))
        self.btn_data_sample.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_sample.setObjectName("btn_data_sample")
        self.flow_layout.addWidget(self.btn_data_sample, 3, 3, 1, 1)
        self.btn_data_new_column = PMToolButton()
        self.btn_data_new_column.setMinimumSize(QSize(80, 60))
        self.btn_data_new_column.setMaximumSize(QSize(80, 60))

        self.btn_data_new_column.setIcon(icon_entirecolumn)
        self.btn_data_new_column.setIconSize(QSize(32, 32))
        self.btn_data_new_column.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_new_column.setObjectName("btn_data_new_column")
        self.flow_layout.addWidget(self.btn_data_new_column, 2, 1, 1, 1)
        self.btn_data_row_filter = PMToolButton()
        self.btn_data_row_filter.setMinimumSize(QSize(80, 60))
        self.btn_data_row_filter.setMaximumSize(QSize(80, 60))

        self.btn_data_row_filter.setIcon(icon_formfilternavigator)
        self.btn_data_row_filter.setIconSize(QSize(32, 32))
        self.btn_data_row_filter.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_row_filter.setObjectName("btn_data_row_filter")
        self.flow_layout.addWidget(self.btn_data_row_filter, 0, 1, 1, 1)
        self.btn_3 = PMToolButton()
        self.btn_3.setMinimumSize(QSize(80, 60))
        self.btn_3.setMaximumSize(QSize(80, 60))

        self.btn_3.setIcon(icon_lc_datasubtotals)
        self.btn_3.setIconSize(QSize(32, 32))
        self.btn_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_3.setObjectName("btn_3")
        self.flow_layout.addWidget(self.btn_3, 6, 4, 1, 1)
        spacerItem3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.flow_layout.addItem(spacerItem3, 11, 3, 1, 1)
        self.btn_data_column_encode = PMToolButton()
        self.btn_data_column_encode.setMinimumSize(QSize(80, 60))
        self.btn_data_column_encode.setMaximumSize(QSize(80, 60))
        icon29 = QIcon()
        icon29.addPixmap(
            QPixmap(":/pyqt/source/images/wordcountdialog.png"), QIcon.Normal, QIcon.Off)
        self.btn_data_column_encode.setIcon(icon29)
        self.btn_data_column_encode.setIconSize(QSize(32, 32))
        self.btn_data_column_encode.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_data_column_encode.setObjectName("btn_data_column_encode")
        self.flow_layout.addWidget(self.btn_data_column_encode, 6, 3, 1, 1)
        self.btn_data_merge_horizontal = PMToolButton()
        self.btn_data_merge_horizontal.setMinimumSize(QSize(80, 60))
        self.btn_data_merge_horizontal.setMaximumSize(QSize(80, 60))

        self.btn_data_merge_horizontal.setIcon(icon_lc_togglemergecells)
        self.btn_data_merge_horizontal.setIconSize(QSize(32, 32))
        self.btn_data_merge_horizontal.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_data_merge_horizontal.setObjectName(
            "btn_data_merge_horizontal")
        self.flow_layout.addWidget(self.btn_data_merge_horizontal, 5, 3, 1, 1)
        self.btn_data_transpose = PMToolButton()
        self.btn_data_transpose.setMinimumSize(QSize(80, 60))
        self.btn_data_transpose.setMaximumSize(QSize(80, 60))

        self.btn_data_transpose.setIcon(icon_lc_datadatapilotrun)
        self.btn_data_transpose.setIconSize(QSize(32, 32))
        self.btn_data_transpose.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_transpose.setObjectName("btn_data_transpose")
        self.flow_layout.addWidget(self.btn_data_transpose, 3, 4, 1, 1)
        self.btn_data_replace = PMToolButton()
        self.btn_data_replace.setMinimumSize(QSize(80, 60))
        self.btn_data_replace.setMaximumSize(QSize(80, 60))

        self.btn_data_replace.setIcon(icon_data_provider)
        self.btn_data_replace.setIconSize(QSize(32, 32))
        self.btn_data_replace.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_replace.setObjectName("btn_data_replace")
        self.flow_layout.addWidget(self.btn_data_replace, 0, 3, 1, 1)
        self.btn_data_missing_value = PMToolButton()
        self.btn_data_missing_value.setMinimumSize(QSize(80, 60))
        self.btn_data_missing_value.setMaximumSize(QSize(80, 60))

        self.btn_data_missing_value.setIcon(icon_dbdistinctvalues)
        self.btn_data_missing_value.setIconSize(QSize(32, 32))
        self.btn_data_missing_value.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_data_missing_value.setObjectName("btn_data_missing_value")
        self.flow_layout.addWidget(self.btn_data_missing_value, 3, 1, 1, 1)
        self.btn_data_column_name = PMToolButton()
        self.btn_data_column_name.setMinimumSize(QSize(80, 60))
        self.btn_data_column_name.setMaximumSize(QSize(80, 60))

        self.btn_data_column_name.setIcon(icon_lc_selectdb)
        self.btn_data_column_name.setIconSize(QSize(32, 32))
        self.btn_data_column_name.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_data_column_name.setObjectName("btn_data_column_name")
        self.flow_layout.addWidget(self.btn_data_column_name, 1, 1, 1, 1)
        self.btn_4 = PMToolButton()
        self.btn_4.setMinimumSize(QSize(80, 60))
        self.btn_4.setMaximumSize(QSize(80, 60))

        self.btn_4.setIcon(icon_lc_accepttrackedchange)
        self.btn_4.setIconSize(QSize(32, 32))
        self.btn_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_4.setObjectName("btn_4")
        self.flow_layout.addWidget(self.btn_4, 7, 4, 1, 1)
        self.btn_data_info = PMToolButton()
        self.btn_data_info.setMinimumSize(QSize(80, 60))
        self.btn_data_info.setMaximumSize(QSize(80, 60))

        self.btn_data_info.setIcon(icon_NavOverFlow_Info)
        self.btn_data_info.setIconSize(QSize(32, 32))
        self.btn_data_info.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_info.setObjectName("btn_data_info")
        self.flow_layout.addWidget(self.btn_data_info, 0, 4, 1, 1)
        self.btn_data_merge_vertical = PMToolButton()
        self.btn_data_merge_vertical.setMinimumSize(QSize(80, 60))
        self.btn_data_merge_vertical.setMaximumSize(QSize(80, 60))

        self.btn_data_merge_vertical.setIcon(icon_mergedocuments)
        self.btn_data_merge_vertical.setIconSize(QSize(32, 32))
        self.btn_data_merge_vertical.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_data_merge_vertical.setObjectName("btn_data_merge_vertical")
        self.flow_layout.addWidget(self.btn_data_merge_vertical, 5, 1, 1, 1)
        self.btn_delete_column = PMToolButton()
        self.btn_delete_column.setMinimumSize(QSize(80, 60))
        self.btn_delete_column.setMaximumSize(QSize(80, 60))

        self.btn_delete_column.setIcon(icon_delete_columns)
        self.btn_delete_column.setIconSize(QSize(32, 32))
        self.btn_delete_column.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_delete_column.setObjectName("btn_delete_column")
        self.flow_layout.addWidget(self.btn_delete_column, 2, 3, 1, 1)
        self.btn_data_sort = PMToolButton()
        self.btn_data_sort.setMinimumSize(QSize(80, 60))
        self.btn_data_sort.setMaximumSize(QSize(80, 60))

        self.btn_data_sort.setIcon(icon_lc_dbviewtablenames)
        self.btn_data_sort.setIconSize(QSize(32, 32))
        self.btn_data_sort.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_sort.setObjectName("btn_data_sort")
        self.flow_layout.addWidget(self.btn_data_sort, 7, 1, 1, 1)
        self.btn_data_partition = PMToolButton()
        self.btn_data_partition.setMinimumSize(QSize(80, 60))
        self.btn_data_partition.setMaximumSize(QSize(80, 60))

        self.btn_data_partition.setIcon(icon_graphicfilterpopart)
        self.btn_data_partition.setIconSize(QSize(32, 32))
        self.btn_data_partition.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_partition.setObjectName("btn_data_partition")
        self.flow_layout.addWidget(self.btn_data_partition, 1, 4, 1, 1)
        self.btn_delete_row = PMToolButton()
        self.btn_delete_row.setMinimumSize(QSize(80, 60))
        self.btn_delete_row.setMaximumSize(QSize(80, 60))

        self.btn_delete_row.setIcon(icon_deleterows)
        self.btn_delete_row.setIconSize(QSize(32, 32))
        self.btn_delete_row.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_delete_row.setObjectName("btn_delete_row")
        self.flow_layout.addWidget(self.btn_delete_row, 2, 4, 1, 1)
        self.btn_data_role = PMToolButton()
        self.btn_data_role.setMinimumSize(QSize(80, 60))
        self.btn_data_role.setMaximumSize(QSize(80, 60))

        self.btn_data_role.setIcon(icon_lc_renametable)
        self.btn_data_role.setIconSize(QSize(32, 32))
        self.btn_data_role.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_role.setObjectName("btn_data_role")
        self.flow_layout.addWidget(self.btn_data_role, 1, 3, 1, 1)
        self.btn_data_column_desc = PMToolButton()
        self.btn_data_column_desc.setMinimumSize(QSize(80, 60))
        self.btn_data_column_desc.setMaximumSize(QSize(80, 60))

        self.btn_data_column_desc.setIcon(icon_lc_formatcolumns)
        self.btn_data_column_desc.setIconSize(QSize(32, 32))
        self.btn_data_column_desc.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_data_column_desc.setObjectName("btn_data_column_desc")
        self.flow_layout.addWidget(self.btn_data_column_desc, 7, 3, 1, 1)
        self.btn_data_standard = PMToolButton()
        self.btn_data_standard.setMinimumSize(QSize(80, 60))
        self.btn_data_standard.setMaximumSize(QSize(80, 60))

        self.btn_data_standard.setIcon(icon_lc_dataarearefresh)
        self.btn_data_standard.setIconSize(QSize(32, 32))
        self.btn_data_standard.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_data_standard.setObjectName("btn_data_standard")
        self.flow_layout.addWidget(self.btn_data_standard, 6, 1, 1, 1)

        self.retranslate_UI()

    def retranslate_UI(self):
        _translate = QCoreApplication.translate
        self.btn_data_filter.setToolTip(_translate("MainWindow", "过滤数据"))
        self.btn_data_filter.setText(_translate("MainWindow", "连接"))
        self.btn_data_sample.setToolTip(_translate("MainWindow", "选择随机抽样"))
        self.btn_data_sample.setText(_translate("MainWindow", "抽样"))
        self.btn_data_new_column.setToolTip(_translate("MainWindow", "堆叠/拆分列"))
        self.btn_data_new_column.setText(_translate("MainWindow", "新增列"))
        self.btn_data_row_filter.setText(_translate("MainWindow", "筛选"))
        self.btn_3.setText(_translate("MainWindow", "重编码范围"))
        self.btn_data_column_encode.setText(_translate("MainWindow", "重编码值"))
        self.btn_data_merge_horizontal.setToolTip(
            _translate("MainWindow", "组合表"))
        self.btn_data_merge_horizontal.setText(
            _translate("MainWindow", "横向合并"))
        self.btn_data_transpose.setToolTip(_translate("MainWindow", "转置数据"))
        self.btn_data_transpose.setText(_translate("MainWindow", "转置数据"))
        self.btn_data_replace.setText(_translate("MainWindow", "查找替换"))
        self.btn_data_missing_value.setText(_translate("MainWindow", "缺失值"))
        self.btn_data_column_name.setText(_translate("MainWindow", "列名处理"))
        self.btn_4.setText(_translate("MainWindow", "转换数据"))
        self.btn_data_info.setToolTip(_translate("MainWindow", "列出表特征"))
        self.btn_data_info.setText(_translate("MainWindow", "数据信息"))
        self.btn_data_merge_vertical.setToolTip(
            _translate("MainWindow", "组合表"))
        self.btn_data_merge_vertical.setText(_translate("MainWindow", "纵向合并"))
        self.btn_delete_column.setText(_translate("MainWindow", "删除列"))
        self.btn_data_sort.setToolTip(_translate("MainWindow", "转置数据"))
        self.btn_data_sort.setText(_translate("MainWindow", "排序数据"))
        self.btn_data_partition.setToolTip(_translate("MainWindow", "分区数据"))
        self.btn_data_partition.setText(_translate("MainWindow", "数据分区"))
        self.btn_delete_row.setText(_translate("MainWindow", "删除行"))
        self.btn_data_role.setText(_translate("MainWindow", "数据角色"))
        self.btn_data_column_desc.setText(_translate("MainWindow", "列出数据"))
        self.btn_data_standard.setText(_translate("MainWindow", "标准化数据"))

    def bind_events(self, app):
        self.btn_data_column_desc.clicked.connect(
            app.data_column_desc_display)  # 列出数据

        # 报告测试
        self.btn_data_column_encode.clicked.connect(app.test_report)

        # 筛选数据
        self.btn_data_filter.clicked.connect(app.data_filter_display)

        # 替换数据
        self.btn_data_replace.clicked.connect(app.data_replace_display)

        # 显示“数据信息”窗口
        self.btn_data_info.clicked.connect(app.data_info_display)

        # 数据角色
        self.btn_data_role.clicked.connect(app.data_role_display)

        # 删除行
        self.btn_delete_row.clicked.connect(app.data_delete_row_display)
        self.btn_delete_column.clicked.connect(app.data_delete_col_display)
        # 纵向合并

        self.btn_data_merge_vertical.clicked.connect(
            app.data_merge_vertical_display)
        # 横向合并

        self.btn_data_merge_horizontal.clicked.connect(
            app.data_merge_horizontal_display)
        # 数据分区
        self.btn_data_partition.clicked.connect(app.data_partition_display)
        # 数据-新增列
        self.btn_data_new_column.clicked.connect(app.data_new_column_display)

        # 数据-缺失值
        self.btn_data_missing_value.clicked.connect(
            app.data_missing_value_display)
        # 数据-筛选和排序
        self.btn_data_sort.clicked.connect(app.data_sort_display)
        # 数据-转置
        self.btn_data_transpose.clicked.connect(app.data_transpose_display)
        # 数据-标准化
        self.btn_data_standard.clicked.connect(app.data_standard_display)
        # 数据-抽样
        self.btn_data_sample.clicked.connect(app.data_sample_display)
        # 数据-列名处理
        self.btn_data_column_name.clicked.connect(app.data_column_name_display)
        # 数据-数据编码
        self.btn_data_column_encode.clicked.connect(
            app.data_column_encode_display)


class PMPageStats(QWidget):
    def __init__(self):
        super().__init__()
        from .resources import icon_wordcountdialog, icon_distributecolumns, icon_dbdistinctvalues, \
            icon_formfilternavigator, icon_lc_closedoc

        self.gridLayout_2 = QGridLayout(self)
        spacerItem4 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 6, 0, 1, 1)
        self.btn_stats_base = PMToolButton(self)
        self.btn_stats_base.setMinimumSize(QSize(80, 60))
        self.btn_stats_base.setMaximumSize(QSize(80, 60))

        self.btn_stats_base.setIcon(icon_wordcountdialog)
        self.btn_stats_base.setIconSize(QSize(32, 32))
        self.btn_stats_base.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.gridLayout_2.addWidget(self.btn_stats_base, 2, 0, 1, 1)
        self.btn_stats_distribution = PMToolButton(self)
        self.btn_stats_distribution.setMinimumSize(QSize(80, 60))
        self.btn_stats_distribution.setMaximumSize(QSize(80, 60))

        self.btn_stats_distribution.setIcon(icon_distributecolumns)
        self.btn_stats_distribution.setIconSize(QSize(32, 32))
        self.btn_stats_distribution.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.gridLayout_2.addWidget(self.btn_stats_distribution, 3, 0, 1, 1)
        self.btn_stats_sum = PMToolButton(self)
        self.btn_stats_sum.setMinimumSize(QSize(80, 60))
        self.btn_stats_sum.setMaximumSize(QSize(80, 60))
        self.btn_stats_sum.setIcon(icon_distributecolumns)
        self.btn_stats_sum.setIconSize(QSize(32, 32))
        self.btn_stats_sum.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.gridLayout_2.addWidget(self.btn_stats_sum, 2, 1, 1, 1)
        self.btn_stats_frequency = PMToolButton(self)
        self.btn_stats_frequency.setMinimumSize(QSize(80, 60))
        self.btn_stats_frequency.setMaximumSize(QSize(80, 60))
        self.btn_stats_frequency.setIcon(icon_distributecolumns)
        self.btn_stats_frequency.setIconSize(QSize(32, 32))
        self.btn_stats_frequency.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.gridLayout_2.addWidget(self.btn_stats_frequency, 2, 2, 1, 1)
        self.btn_stats_corr = PMToolButton(self)
        self.btn_stats_corr.setMinimumSize(QSize(80, 60))
        self.btn_stats_corr.setMaximumSize(QSize(80, 60))
        self.btn_stats_corr.setIcon(icon_distributecolumns)
        self.btn_stats_corr.setIconSize(QSize(32, 32))
        self.btn_stats_corr.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_stats_corr.setObjectName("btn_stats_corr")
        self.gridLayout_2.addWidget(self.btn_stats_corr, 3, 1, 1, 1)
        self.btn_stats_t = PMToolButton(self)
        self.btn_stats_t.setMinimumSize(QSize(80, 60))
        self.btn_stats_t.setMaximumSize(QSize(80, 60))
        self.btn_stats_t.setIcon(icon_distributecolumns)
        self.btn_stats_t.setIconSize(QSize(32, 32))
        self.btn_stats_t.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_stats_t.setObjectName("btn_stats_t")
        self.gridLayout_2.addWidget(self.btn_stats_t, 3, 2, 1, 1)
        self.btn_stats_missing_value = PMToolButton(self)
        self.btn_stats_missing_value.setMinimumSize(QSize(80, 60))
        self.btn_stats_missing_value.setMaximumSize(QSize(80, 60))
        self.btn_stats_missing_value.setIcon(icon_dbdistinctvalues)
        self.btn_stats_missing_value.setIconSize(QSize(32, 32))
        self.btn_stats_missing_value.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_stats_missing_value.setObjectName("btn_stats_missing_value")
        self.gridLayout_2.addWidget(self.btn_stats_missing_value, 4, 0, 1, 1)
        self.btn_stats_except_value = PMToolButton(self)
        self.btn_stats_except_value.setMinimumSize(QSize(80, 60))
        self.btn_stats_except_value.setMaximumSize(QSize(80, 60))

        self.btn_stats_except_value.setIcon(icon_lc_closedoc)
        self.btn_stats_except_value.setIconSize(QSize(32, 32))
        self.btn_stats_except_value.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_stats_except_value.setObjectName("btn_stats_except_value")
        self.gridLayout_2.addWidget(self.btn_stats_except_value, 4, 2, 1, 1)
        self.btn_stats_unique_value = PMToolButton(self)
        self.btn_stats_unique_value.setMinimumSize(QSize(80, 60))
        self.btn_stats_unique_value.setMaximumSize(QSize(80, 60))
        self.btn_stats_unique_value.setIcon(icon_formfilternavigator)
        self.btn_stats_unique_value.setIconSize(QSize(32, 32))
        self.btn_stats_unique_value.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_stats_unique_value.setObjectName("btn_stats_unique_value")
        self.gridLayout_2.addWidget(self.btn_stats_unique_value, 4, 1, 1, 1)
        self.translate()

    def translate(self):
        _translate = QCoreApplication.translate
        self.btn_stats_base.setToolTip(_translate("MainWindow", "描述数据特征"))
        self.btn_stats_base.setText(_translate("MainWindow", "描述统计"))
        self.btn_stats_distribution.setText(_translate("MainWindow", "数据分布"))
        self.btn_stats_sum.setText(_translate("MainWindow", "汇总统计量"))
        self.btn_stats_frequency.setText(_translate("MainWindow", "单因子频数"))
        self.btn_stats_corr.setText(_translate("MainWindow", "相关分析"))
        self.btn_stats_t.setText(_translate("MainWindow", "t检验"))
        self.btn_stats_missing_value.setToolTip(
            _translate("MainWindow", "描述缺失数据"))
        self.btn_stats_missing_value.setText(_translate("MainWindow", "缺失数据"))
        self.btn_stats_except_value.setText(_translate("MainWindow", "异常值"))
        self.btn_stats_unique_value.setText(_translate("MainWindow", "唯一值"))

    def bind_events(self, app):
        self.btn_stats_base.clicked.connect(
            app.stats_base_display)  # 显示“描述统计”窗口


class PMPagePlot(QWidget):
    def __init__(self):
        super().__init__()
        from .resources import icon_dbdistinctvalues, icon_netfill, icon_stockcolumns, icon_bubble, icon_areas, \
            icon_nostackdirectboth_52x60, icon_pie, icon_areaspiled, icon_columns_52x60

        self.gridLayout_3 = QGridLayout(self)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_plot_box = PMToolButton(self)
        self.btn_plot_box.setMinimumSize(QSize(80, 60))
        self.btn_plot_box.setMaximumSize(QSize(80, 60))

        self.btn_plot_box.setIcon(icon_stockcolumns)
        self.btn_plot_box.setIconSize(QSize(32, 32))
        self.btn_plot_box.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_box.setObjectName("btn_plot_box")
        self.gridLayout_3.addWidget(self.btn_plot_box, 1, 1, 1, 1)
        self.btn_plot_line = PMToolButton(self)
        self.btn_plot_line.setMinimumSize(QSize(80, 60))
        self.btn_plot_line.setMaximumSize(QSize(80, 60))

        self.btn_plot_line.setIcon(icon_nostackdirectboth_52x60)
        self.btn_plot_line.setIconSize(QSize(32, 32))
        self.btn_plot_line.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_line.setObjectName("btn_plot_line")
        self.gridLayout_3.addWidget(self.btn_plot_line, 0, 1, 1, 1)
        spacerItem5 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem5, 5, 1, 1, 1)
        self.btn_plot_radar = PMToolButton(self)
        self.btn_plot_radar.setMinimumSize(QSize(80, 60))
        self.btn_plot_radar.setMaximumSize(QSize(80, 60))
        self.btn_plot_radar.setIcon(icon_netfill)
        self.btn_plot_radar.setIconSize(QSize(32, 32))
        self.btn_plot_radar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_radar.setObjectName("btn_plot_radar")
        self.gridLayout_3.addWidget(self.btn_plot_radar, 3, 0, 1, 1)
        self.btn_plot_scotter = PMToolButton(self)
        self.btn_plot_scotter.setMinimumSize(QSize(80, 60))
        self.btn_plot_scotter.setMaximumSize(QSize(80, 60))

        self.btn_plot_scotter.setIcon(icon_bubble)
        self.btn_plot_scotter.setIconSize(QSize(32, 32))
        self.btn_plot_scotter.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_scotter.setObjectName("btn_plot_scotter")
        self.gridLayout_3.addWidget(self.btn_plot_scotter, 0, 2, 1, 1)
        self.btn_plot_area = PMToolButton(self)
        self.btn_plot_area.setMinimumSize(QSize(80, 60))
        self.btn_plot_area.setMaximumSize(QSize(80, 60))

        self.btn_plot_area.setIcon(icon_areas)
        self.btn_plot_area.setIconSize(QSize(32, 32))
        self.btn_plot_area.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_area.setObjectName("btn_plot_area")
        self.gridLayout_3.addWidget(self.btn_plot_area, 2, 0, 1, 1)
        self.btn_plot_pie = PMToolButton(self)
        self.btn_plot_pie.setMinimumSize(QSize(80, 60))
        self.btn_plot_pie.setMaximumSize(QSize(80, 60))
        self.btn_plot_pie.setIcon(icon_pie)
        self.btn_plot_pie.setIconSize(QSize(32, 32))
        self.btn_plot_pie.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_pie.setObjectName("btn_plot_pie")
        self.gridLayout_3.addWidget(self.btn_plot_pie, 1, 2, 1, 1)
        self.btn_plot_heap = PMToolButton(self)
        self.btn_plot_heap.setMinimumSize(QSize(80, 60))
        self.btn_plot_heap.setMaximumSize(QSize(80, 60))

        self.btn_plot_heap.setIcon(icon_areaspiled)
        self.btn_plot_heap.setIconSize(QSize(32, 32))
        self.btn_plot_heap.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_heap.setObjectName("btn_plot_heap")
        self.gridLayout_3.addWidget(self.btn_plot_heap, 2, 2, 1, 1)
        self.btn_plot_hist = PMToolButton(self)
        self.btn_plot_hist.setMinimumSize(QSize(80, 60))
        self.btn_plot_hist.setMaximumSize(QSize(80, 60))
        self.btn_plot_hist.setIcon(icon_columns_52x60)
        self.btn_plot_hist.setIconSize(QSize(32, 32))
        self.btn_plot_hist.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_hist.setObjectName("btn_plot_hist")
        self.gridLayout_3.addWidget(self.btn_plot_hist, 0, 0, 1, 1)
        self.btn_plot_bar = PMToolButton(self)
        self.btn_plot_bar.setMinimumSize(QSize(80, 60))
        self.btn_plot_bar.setMaximumSize(QSize(80, 60))
        self.btn_plot_bar.setIcon(icon_columns_52x60)
        self.btn_plot_bar.setIconSize(QSize(32, 32))
        self.btn_plot_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_bar.setObjectName("btn_plot_bar")
        self.gridLayout_3.addWidget(self.btn_plot_bar, 1, 0, 1, 1)
        self.btn_plot_missing_value = PMToolButton(self)
        self.btn_plot_missing_value.setMinimumSize(QSize(80, 60))
        self.btn_plot_missing_value.setMaximumSize(QSize(80, 60))
        self.btn_plot_missing_value.setIcon(icon_dbdistinctvalues)
        self.btn_plot_missing_value.setIconSize(QSize(32, 32))
        self.btn_plot_missing_value.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_plot_missing_value.setObjectName("btn_plot_missing_value")
        self.gridLayout_3.addWidget(self.btn_plot_missing_value, 3, 2, 1, 1)
        self.btn_plot_radar_3 = PMToolButton(self)
        self.btn_plot_radar_3.setMinimumSize(QSize(80, 60))
        self.btn_plot_radar_3.setMaximumSize(QSize(80, 60))
        self.btn_plot_radar_3.setIcon(icon_netfill)
        self.btn_plot_radar_3.setIconSize(QSize(32, 32))
        self.btn_plot_radar_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_radar_3.setObjectName("btn_plot_radar_3")
        self.gridLayout_3.addWidget(self.btn_plot_radar_3, 2, 1, 1, 1)
        self.btn_plot_radar_4 = PMToolButton(self)
        self.btn_plot_radar_4.setMinimumSize(QSize(80, 60))
        self.btn_plot_radar_4.setMaximumSize(QSize(80, 60))
        self.btn_plot_radar_4.setIcon(icon_netfill)
        self.btn_plot_radar_4.setIconSize(QSize(32, 32))
        self.btn_plot_radar_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_plot_radar_4.setObjectName("btn_plot_radar_4")
        self.gridLayout_3.addWidget(self.btn_plot_radar_4, 3, 1, 1, 1)
        self.translate()

    def translate(self):
        _translate = QCoreApplication.translate
        self.btn_plot_box.setText(_translate("MainWindow", "盒形图"))
        self.btn_plot_line.setText(_translate("MainWindow", "折线图"))
        self.btn_plot_radar.setText(_translate("MainWindow", "雷达图"))
        self.btn_plot_scotter.setText(_translate("MainWindow", "散点图"))
        self.btn_plot_area.setText(_translate("MainWindow", "面积图"))
        self.btn_plot_pie.setText(_translate("MainWindow", "饼图"))
        self.btn_plot_heap.setText(_translate("MainWindow", "热力图"))
        self.btn_plot_hist.setText(_translate("MainWindow", "直方图"))
        self.btn_plot_bar.setText(_translate("MainWindow", "条形图"))
        self.btn_plot_missing_value.setText(_translate("MainWindow", "缺失值"))
        self.btn_plot_radar_3.setText(_translate("MainWindow", "马赛克图"))
        self.btn_plot_radar_4.setText(_translate("MainWindow", "文本地图"))

    def bind_events(self, app):
        self.btn_plot_hist.clicked.connect(
            app.plot_frame_display)  # 打开"数据可视化-直方图"窗口


class PMPageModel(QWidget):
    def __init__(self):
        super().__init__()
        from .resources import icon_nostackdirectboth_52x60, icon_delete_columns, icon_formfilternavigator
        self.gridLayout_4 = QGridLayout(self)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_model_cnn = PMToolButton(self)
        self.btn_model_cnn.setMinimumSize(QSize(80, 60))
        self.btn_model_cnn.setMaximumSize(QSize(80, 60))
        self.btn_model_cnn.setIcon(icon_nostackdirectboth_52x60)
        self.btn_model_cnn.setIconSize(QSize(32, 32))
        self.btn_model_cnn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_cnn.setObjectName("btn_model_cnn")
        self.gridLayout_4.addWidget(self.btn_model_cnn, 1, 2, 1, 1)
        self.btn_model_time_seires = PMToolButton(self)
        self.btn_model_time_seires.setMinimumSize(QSize(80, 60))
        self.btn_model_time_seires.setMaximumSize(QSize(80, 60))
        self.btn_model_time_seires.setIcon(icon_delete_columns)
        self.btn_model_time_seires.setIconSize(QSize(32, 32))
        self.btn_model_time_seires.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_model_time_seires.setObjectName("btn_model_time_seires")
        self.gridLayout_4.addWidget(self.btn_model_time_seires, 1, 1, 1, 1)
        self.btn_model_scorecard = PMToolButton(self)
        self.btn_model_scorecard.setMinimumSize(QSize(80, 60))
        self.btn_model_scorecard.setMaximumSize(QSize(80, 60))
        self.btn_model_scorecard.setIcon(icon_nostackdirectboth_52x60)
        self.btn_model_scorecard.setIconSize(QSize(32, 32))
        self.btn_model_scorecard.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_scorecard.setObjectName("btn_model_scorecard")
        self.gridLayout_4.addWidget(self.btn_model_scorecard, 1, 0, 1, 1)
        self.btn_model_3 = PMToolButton(self)
        self.btn_model_3.setMinimumSize(QSize(80, 60))
        self.btn_model_3.setMaximumSize(QSize(80, 60))
        self.btn_model_3.setIcon(icon_nostackdirectboth_52x60)
        self.btn_model_3.setIconSize(QSize(32, 32))
        self.btn_model_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_3.setObjectName("btn_model_3")
        self.gridLayout_4.addWidget(self.btn_model_3, 2, 2, 1, 1)
        self.btn_model_tree = PMToolButton(self)
        self.btn_model_tree.setMinimumSize(QSize(80, 60))
        self.btn_model_tree.setMaximumSize(QSize(80, 60))
        self.btn_model_tree.setIcon(icon_formfilternavigator)
        self.btn_model_tree.setIconSize(QSize(32, 32))
        self.btn_model_tree.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_tree.setObjectName("btn_model_tree")
        self.gridLayout_4.addWidget(self.btn_model_tree, 0, 2, 1, 1)
        self.btn_model_1 = PMToolButton(self)
        self.btn_model_1.setMinimumSize(QSize(80, 60))
        self.btn_model_1.setMaximumSize(QSize(80, 60))
        self.btn_model_1.setIcon(icon_nostackdirectboth_52x60)
        self.btn_model_1.setIconSize(QSize(32, 32))
        self.btn_model_1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_1.setObjectName("btn_model_1")
        self.gridLayout_4.addWidget(self.btn_model_1, 2, 0, 1, 1)
        spacerItem6 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem6, 5, 1, 1, 1)
        self.btn_model_2 = PMToolButton(self)
        self.btn_model_2.setMinimumSize(QSize(80, 60))
        self.btn_model_2.setMaximumSize(QSize(80, 60))
        self.btn_model_2.setIcon(icon_nostackdirectboth_52x60)
        self.btn_model_2.setIconSize(QSize(32, 32))
        self.btn_model_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_2.setObjectName("btn_model_2")
        self.gridLayout_4.addWidget(self.btn_model_2, 2, 1, 1, 1)
        self.btn_model_logist = PMToolButton(self)
        self.btn_model_logist.setMinimumSize(QSize(80, 60))
        self.btn_model_logist.setMaximumSize(QSize(80, 60))
        self.btn_model_logist.setIcon(icon_formfilternavigator)
        self.btn_model_logist.setIconSize(QSize(32, 32))
        self.btn_model_logist.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_logist.setObjectName("btn_model_logist")
        self.gridLayout_4.addWidget(self.btn_model_logist, 0, 1, 1, 1)
        self.btn_model_linear_regression = PMToolButton(self)
        self.btn_model_linear_regression.setMinimumSize(QSize(80, 60))
        self.btn_model_linear_regression.setMaximumSize(QSize(80, 60))
        self.btn_model_linear_regression.setIcon(icon_formfilternavigator)
        self.btn_model_linear_regression.setIconSize(QSize(32, 32))
        self.btn_model_linear_regression.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_model_linear_regression.setObjectName(
            "btn_model_linear_regression")
        self.gridLayout_4.addWidget(
            self.btn_model_linear_regression, 0, 0, 1, 1)
        self.btn_model_4 = PMToolButton(self)
        self.btn_model_4.setMinimumSize(QSize(80, 60))
        self.btn_model_4.setMaximumSize(QSize(80, 60))
        self.btn_model_4.setIcon(icon_nostackdirectboth_52x60)
        self.btn_model_4.setIconSize(QSize(32, 32))
        self.btn_model_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_model_4.setObjectName("btn_model_4")
        self.gridLayout_4.addWidget(self.btn_model_4, 3, 0, 1, 1)
        self.translate()

    def translate(self):
        _translate = QCoreApplication.translate
        self.btn_model_cnn.setText(_translate("MainWindow", "神经网络"))
        self.btn_model_time_seires.setText(_translate("MainWindow", "时间序列"))
        self.btn_model_scorecard.setText(_translate("MainWindow", "评分卡"))
        self.btn_model_3.setText(_translate("MainWindow", "聚类分析"))
        self.btn_model_tree.setText(_translate("MainWindow", "决策树"))
        self.btn_model_1.setText(_translate("MainWindow", "生存分析"))
        self.btn_model_2.setText(_translate("MainWindow", "多元分析"))
        self.btn_model_logist.setText(_translate("MainWindow", "逻辑回归"))
        self.btn_model_linear_regression.setText(
            _translate("MainWindow", "线性模型"))
        self.btn_model_4.setText(_translate("MainWindow", "预测"))

    def bind_events(self, app):
        self.btn_model_linear_regression.clicked.connect(
            app.model_frame_display)  # 展示模型页面
        self.btn_model_tree.clicked.connect(
            app.model_tree_display)  # 打开"模型-决策树"窗口


class PMPage(QWidget):
    def __init__(self):
        super().__init__()
        from .resources import icon_formfilternavigator, icon_nostackdirectboth_52x60, icon_columns_52x60

        self.gridLayout_7 = QGridLayout(self)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.btn_assess_auc = PMToolButton(self)
        self.btn_assess_auc.setMinimumSize(QSize(80, 60))
        self.btn_assess_auc.setMaximumSize(QSize(80, 60))
        self.btn_assess_auc.setIcon(icon_formfilternavigator)
        self.btn_assess_auc.setIconSize(QSize(32, 32))
        self.btn_assess_auc.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_assess_auc.setObjectName("btn_assess_auc")
        self.gridLayout_7.addWidget(self.btn_assess_auc, 1, 3, 1, 1)
        self.btn_assess_feature_select = PMToolButton(self)
        self.btn_assess_feature_select.setMinimumSize(QSize(80, 60))
        self.btn_assess_feature_select.setMaximumSize(QSize(80, 60))
        self.btn_assess_feature_select.setIcon(icon_formfilternavigator)
        self.btn_assess_feature_select.setIconSize(QSize(32, 32))
        self.btn_assess_feature_select.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.btn_assess_feature_select.setObjectName(
            "btn_assess_feature_select")
        self.gridLayout_7.addWidget(self.btn_assess_feature_select, 0, 3, 1, 1)
        self.btn_assess_iv = PMToolButton(self)
        self.btn_assess_iv.setMinimumSize(QSize(80, 60))
        self.btn_assess_iv.setMaximumSize(QSize(80, 60))
        self.btn_assess_iv.setIcon(icon_columns_52x60)
        self.btn_assess_iv.setIconSize(QSize(32, 32))
        self.btn_assess_iv.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_assess_iv.setObjectName("btn_assess_iv")
        self.gridLayout_7.addWidget(self.btn_assess_iv, 0, 1, 1, 1)
        self.btn_access_fine = PMToolButton(self)
        self.btn_access_fine.setMinimumSize(QSize(80, 60))
        self.btn_access_fine.setMaximumSize(QSize(80, 60))
        self.btn_access_fine.setIcon(icon_formfilternavigator)
        self.btn_access_fine.setIconSize(QSize(32, 32))
        self.btn_access_fine.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_access_fine.setObjectName("btn_access_fine")
        self.gridLayout_7.addWidget(self.btn_access_fine, 1, 0, 1, 1)
        self.btn_assess_psi = PMToolButton(self)
        self.btn_assess_psi.setMinimumSize(QSize(80, 60))
        self.btn_assess_psi.setMaximumSize(QSize(80, 60))
        self.btn_assess_psi.setIcon(icon_formfilternavigator)
        self.btn_assess_psi.setIconSize(QSize(32, 32))
        self.btn_assess_psi.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_assess_psi.setObjectName("btn_assess_psi")
        self.gridLayout_7.addWidget(self.btn_assess_psi, 1, 1, 1, 1)
        spacerItem7 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem7, 3, 1, 1, 1)
        self.btn_assess_woe = PMToolButton(self)
        self.btn_assess_woe.setMinimumSize(QSize(80, 60))
        self.btn_assess_woe.setMaximumSize(QSize(80, 60))
        self.btn_assess_woe.setIcon(icon_nostackdirectboth_52x60)
        self.btn_assess_woe.setIconSize(QSize(32, 32))
        self.btn_assess_woe.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_assess_woe.setObjectName("btn_assess_woe")
        self.gridLayout_7.addWidget(self.btn_assess_woe, 0, 0, 1, 1)
        self.btn_access_model = PMToolButton(self)
        self.btn_access_model.setMinimumSize(QSize(80, 60))
        self.btn_access_model.setMaximumSize(QSize(80, 60))
        self.btn_access_model.setIcon(icon_formfilternavigator)
        self.btn_access_model.setIconSize(QSize(32, 32))
        self.btn_access_model.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_access_model.setObjectName("btn_access_model")
        self.gridLayout_7.addWidget(self.btn_access_model, 2, 0, 1, 1)
        self.translate()

    def translate(self):
        _translate = QCoreApplication.translate
        self.btn_assess_auc.setText(_translate("MainWindow", "AUC"))
        self.btn_assess_feature_select.setText(
            _translate("MainWindow", "特征选择"))
        self.btn_assess_iv.setText(_translate("MainWindow", "IV"))
        self.btn_access_fine.setText(_translate("MainWindow", "特征分箱"))
        self.btn_assess_psi.setText(_translate("MainWindow", "PSI"))
        self.btn_assess_woe.setText(_translate("MainWindow", "WOE"))
        self.btn_access_model.setText(_translate("MainWindow", "模型评价"))

    def bind_events(self, app: QMainWindow):
        self.btn_assess_woe.clicked.connect(app.model_woe_display)


class ExtInfoWidget(QWidget):
    """
    扩展信息组件,扩展列表中的一项
    """

    def __init__(self, parent, ext, ext_manager):
        """
        parent:父组件
        ext:信息组件对应扩展
        ext_manager:扩展管理器
        """
        super().__init__(parent)
        self.ext = ext
        self.ext_manager = ext_manager
        self.page = parent
        self.init_ui()

    def uninstall(self):
        """卸载操作"""
        self.ext_manager.uninstall(self.ext.id_)
        self.page.init_extensions()

    def show_menu(self, p):
        """右键菜单"""
        menu = QMenu(self)
        action_info = menu.addAction('卸载')
        action_info.triggered.connect(self.uninstall)
        menu.exec_(QCursor.pos())

    def info(self):
        """展示扩展信息(扩展商店中的)"""
        url = f'http://py2cn.com/extensions?name={self.ext.info.name}'
        webbrowser.open(url)

    def init_ui(self):
        """初始化ui"""
        self.layout = QHBoxLayout(self)

        # 扩展图标
        img = QLabel(self)
        img_path = os.path.join(get_root_dir(
        ), 'extensions/packages/', self.ext.info.name, self.ext.info.icon)
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaledToHeight(50)
        img.setPixmap(pixmap)
        self.layout.addWidget(img)

        # 扩展名称
        ext_name = QLabel(self)
        ext_name.setText(self.ext.info.display_name)
        self.layout.addWidget(ext_name)

        # 设置菜单模式,关联菜单事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setLayout(self.layout)
        self.show()

    def mouseDoubleClickEvent(self, *args):
        self.info()


class PMPageExt(QWidget):
    """
    扩展选项卡页
    """

    def __init__(self, main_window):
        """
        main_window:主窗口
        """
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.main_window = main_window
        self.ext_manager = extensions_manager
        self.init_ui()

    # def sizeHint(self) -> QSize:
    #     return QSize(100,300)
    # def resizeEvent(self, a0: QResizeEvent) -> None:
    #     self.setMaximumWidth(300)
    #     super().resizeEvent(a0)

    def install(self):
        """安装扩展"""
        path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption='请选择要安装的压缩包',
            directory='C:/',
            filter='所有文件(*.*);;zip文件(*.zip)',
            initialFilter='zip文件(*.zip)'
        )
        self.ext_manager.install(path)
        # 刷新扩展列表
        self.init_extensions()

    def init_extensions(self):
        self.ext_list.clear()  # 先清空
        for ext in self.ext_manager.extensions:
            item = QListWidgetItem(self.ext_list, 0)
            item.setSizeHint(QSize(self.ext_list.width() - 20, 50))
            w = ExtInfoWidget(self, ext, self.ext_manager)
            self.ext_list.addItem(item)
            self.ext_list.setItemWidget(item, w)

    def init_ui(self):
        """初始化ui"""
        self.layout = QVBoxLayout(self)

        # 扩展列表
        self.ext_list = QListWidget(self)
        self.init_extensions()
        self.ext_list.show()
        self.layout.addWidget(self.ext_list)

        # 从本地安装按钮
        self.install_btn = QPushButton(self)
        self.install_btn.setText('安装 - 从本地')
        self.install_btn.clicked.connect(self.install)
        self.layout.addWidget(self.install_btn)

        self.setLayout(self.layout)


class PMWorkspaceInspectWidget(QTableWidget):
    def __init__(self, parnet=None):
        super().__init__(parent=None)
        self.setRowCount(4)
        self.setColumnCount(10)
        for i, name in enumerate(['名称', '类型', '大小', '值']):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(name))
            # self.setCellWidget()
        # self.setItem(0,0,QTableWidgetItem('123123123'))

    def set_data_view(self):
        pass


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    sa = PMWorkspaceInspectWidget()
    sa.show()
    sys.exit(app.exec())
