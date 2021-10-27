import subprocess
import sys
from PySide2.QtWidgets import QFrame, QTableWidgetItem, QTableWidget, QMessageBox, QDialog, QDesktopWidget, QHeaderView, \
    QProgressDialog
from PySide2.QtGui import QCloseEvent
from PySide2.QtCore import Signal, Qt, QUrl, QPropertyAnimation
from lib.ui.pm_marketplace.main import Ui_Form as marketplace_Ui_Form

from widgets import PMGOneShotThreadRunner


class MarketplaceForm(QDialog, marketplace_Ui_Form):
    def __init__(self, parent=None):
        super(MarketplaceForm, self).__init__(parent)
        self.setupUi(self)
