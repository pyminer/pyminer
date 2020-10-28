# coding=utf-8
import os
import sys
import logging
import webbrowser
import time
import numpy as np
import pandas as pd
from sklearn import tree
# from IPython.display import Image
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # 数据标准化

# 导入PyQt5模块
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QDialog, QMessageBox, QTableWidgetItem

# 导入模型相关操作模块
from data_miner.ui.model.model_woe_result import Ui_Form as ModelWoeIVResult_Ui_Form
from data_miner.ui.model.model_woe import Ui_Form as ModelWoe_Ui_Form
from data_miner.ui.model.model_frame import Ui_Form as ModelFrame_Ui_Form
from data_miner.ui.model.model_tree import Ui_Form as ModelTree_Ui_Form

# 定义日志输出格式
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)


class ModelFrameForm(QWidget):
    """
    "新建窗口"
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = ModelFrame_Ui_Form()
        self.__ui.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class ModelFrameForm(QWidget, ModelFrame_Ui_Form):
    """
    打开"关于"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


class ModelTreeForm(QDialog, ModelTree_Ui_Form):
    """
    打开"模型-决策树"窗口
    """
    signal_output = pyqtSignal(str, str)  # 自定义信号，用于传递输出结果的名称、路径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()
        self.current_dataset = pd.DataFrame()
        self.current_dataset_columns = []
        self.tree_count = 0

        self.lineEdit_result_path.setText(output_dir)
        self.pushButton_dependent_add.clicked.connect(self.dependent_add)
        self.pushButton_dependent_del.clicked.connect(self.dependent_del)

        self.pushButton_independent_add.clicked.connect(self.independent_add)
        self.pushButton_independent_up.clicked.connect(self.independent_up)
        self.pushButton_independent_down.clicked.connect(self.independent_down)
        self.pushButton_independent_del.clicked.connect(self.independent_del)

        self.pushButton_ok.clicked.connect(self.model_tree)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_help.clicked.connect(self.get_help)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    #  ================================自定义槽函数=========================
    def get_help(self):
        """
        打开帮助页面
        """
        try:
            webbrowser.get('chrome').open_new_tab("http://www.py2cn.com")
        except Exception as e:
            webbrowser.open_new_tab("http://www.py2cn.com")

    def model_tree(self):
        self.tree_count += 1  # 用户生成决策树名称，根据第几次调用决策树进行命名
        result_name = "tree_" + str(self.tree_count)
        result_png = result_name + '.png'
        result_png_path = output_dir + '\\' + result_png
        print('result_name', result_name)
        print('result_png_path', result_png_path)

        if len(self.lineEdit_result_path.text().strip()) == 0:
            QMessageBox.information(self, "注意", "决策树路径不能为空", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return

        result_path = self.lineEdit_result_path.text() + r'/' + result_name + '.html'
        print(result_path)

        # 可视化决策树
        data = self.current_dataset
        # 获取已选变量
        var_list = []
        count = self.listWidget_independent.count()
        for i in range(count):
            var_list.append(self.listWidget_independent.item(i).text())

        data_x = data[var_list]
        print(data_x)
        data_y = data[self.listWidget_dependent.item(0).text()]

        # 获取用户设置的参数
        train_size = self.doubleSpinBox_train_size.value()
        random_state = self.lineEdit_random_state.value()
        min_samples_leaf = self.spinBox_min_samples_leaf.value()
        max_depth = self.spinBox_max_depth.value()
        criterion = self.comboBox_criterion.currentText().lower()
        min_samples_split = self.spinBox_min_samples_split.value()
        train_X, test_X, train_y, test_y = train_test_split(data_x
                                                            , data_y
                                                            , train_size=train_size
                                                            , random_state=random_state)

        model_tree = tree.DecisionTreeClassifier(criterion=criterion  # gini或者entropy,前者是基尼系数，后者是信息熵。
                                                 , splitter="best"
                                                 # best or random 前者是在所有特征中找最好的切分点 后者是在部分特征中，默认的”best”适合样本量不大的时候，而如果样本数据量非常大，此时决策树构建推荐”random” 。
                                                 , max_features=None  # None（所有），log2，sqrt，N  特征小于50的时候一般使用所有的
                                                 , min_samples_leaf=min_samples_leaf  # 最小叶子节点数
                                                 , max_depth=max_depth
                                                 # int or None, optional (default=None) 设置决策随机森林中的决策树的最大深度，深度越大，越容易过拟合，推荐树的深度为：5-20之间。
                                                 , min_samples_split=min_samples_split
                                                 # 设置结点的最小样本数量，当样本数量可能小于此值时，结点将不会在划分。
                                                 , max_leaf_nodes=None  # 通过限制最大叶子节点数，可以防止过拟合，默认是"None”，即不限制最大的叶子节点数。
                                                 )
        model_tree = model_tree.fit(train_X, train_y)

        score = model_tree.score(test_X, test_y)  # 返回预测的准确度accuracy
        print(score)
        # feature_name = ["酒精", "苹果酸", "灰", "灰的碱性", "镁", "总酚", "类黄酮", "非黄烷类酚类", "花青素", "颜色强度", "色调", "od280/od315稀疏葡萄酒",
        #                 "脯氨酸"]
        print("开始执行决策树")
        dot_tree = tree.export_graphviz(model_tree
                                        , out_file=None
                                        # , feature_names=feature_name
                                        # , class_names=["琴酒", "雪莉", "贝尔莫得"]
                                        , filled=True  # 填充颜色
                                        , rounded=True  # 画出的方块无棱角
                                        , special_characters=True
                                        )

        os.environ["PATH"] += root_dir + r'\features\plugins\graphviz-2.38\release\bin'
        graph = pydotplus.graph_from_dot_data(dot_tree)
        # img = Image(graph.create_png())
        graph.write_png(result_png_path)
        print("图片已生成！")

        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>结果</title>
</head>
<body>
<img border="0" src=" """ + result_png_path + """ " alt="决策树结果" >
</body>
</html>
        """
        with open(result_path, 'w') as f:
            f.write(html)
            print("写入完成")
            f.close()
        print("开始发射信号")
        self.signal_result.emit(result_name, result_path)  # 发射信号
        self.close()

    def dependent_add(self):
        items = self.listWidget_var.selectedItems()
        for item in items:
            self.listWidget_dependent.addItem(item.text())

    def dependent_del(self):
        items = self.listWidget_dependent.selectedItems()
        for item in items:
            row = self.listWidget_dependent.row(item)
            self.listWidget_dependent.removeItemWidget(self.listWidget_dependent.takeItem(row))

    def independent_add(self):
        items = self.listWidget_var.selectedItems()
        for item in items:
            self.listWidget_independent.addItem(item.text())

    def independent_up(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_independent.count()
        for i in range(count):
            var_list.append(self.listWidget_independent.item(i).text())
        row = self.listWidget_independent.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row - 1]
        var_list[row - 1] = temp
        # 清空当前listWidget
        self.listWidget_independent.clear()
        # 重新添加新项
        self.listWidget_independent.addItems(var_list)

    def independent_down(self):
        var_list = []
        # 获取listwidget中条目数
        count = self.listWidget_independent.count()
        for i in range(count):
            var_list.append(self.listWidget_independent.item(i).text())
        row = self.listWidget_independent.currentRow()
        print("row:", row)
        temp = var_list[row]
        var_list[row] = var_list[row + 1]
        var_list[row + 1] = temp
        # 清空当前listWidget
        self.listWidget_independent.clear()
        # 重新添加新项
        self.listWidget_independent.addItems(var_list)

    def independent_del(self):
        items = self.listWidget_independent.selectedItems()
        for item in items:
            row = self.listWidget_independent.row(item)
            self.listWidget_independent.removeItemWidget(self.listWidget_independent.takeItem(row))


class ModelWoeForm(QDialog, ModelWoe_Ui_Form):
    """
    打开"模型-WOE/IV"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.center()

        self.current_dataset = pd.DataFrame()
        self.all_dataset = ''
        self.current_dataset_name = ''
        self.current_dataset_columns = ''
        self.current_dataset_path = ''  # 当前数据对应路径

        self.pushButton_next.clicked.connect(self.calc_woe)
        self.toolButton_output_path.triggered.connect(self.slot_change_output_path)

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))

    def slot_change_output_path(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输出文件位置", output_dir)
        self.lineEdit_output_path.setText(directory)

    def calc_woe(self):
        if os.path.isfile(output_dir + r"\features_detail.csv"):
            feature_detail = pd.read_csv(output_dir + r"\features_detail.csv")
        else:
            feature_detail = calc_woe_iv.woe(self.current_dataset)
        self.flush_preview(feature_detail)

    def flush_preview(self, dataset):
        if any(dataset):
            input_table_rows = dataset.head(100).shape[0]
            input_table_colunms = dataset.shape[1]
            input_table_header = dataset.columns.values.tolist()
            self.tableWidget_dataset.setColumnCount(input_table_colunms)
            self.tableWidget_dataset.setRowCount(input_table_rows)
            self.tableWidget_dataset.setHorizontalHeaderLabels(input_table_header)

        # 数据预览窗口
        for i in range(input_table_rows):
            input_table_rows_values = dataset.iloc[[i]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            for j in range(input_table_colunms):
                input_table_items_list = input_table_rows_values_list[j]

                input_table_items = str(input_table_items_list)
                newItem = QTableWidgetItem(input_table_items)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_dataset.setItem(i, j, newItem)


class ModelWoeResultForm(QWidget):
    """
    打开"关于"窗口
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = ModelWoeIVResult_Ui_Form()
        self.__ui.setupUi(self)
        self.center()

    def keyPressEvent(self, e):
        """
        按键盘Escape退出当前窗口
        @param e:
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


# ====================================窗体测试程序============================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ModelFrameForm()
    form.show()
    sys.exit(app.exec_())
