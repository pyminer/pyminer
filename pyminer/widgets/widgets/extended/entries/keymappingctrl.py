from PySide2.QtCore import Qt
from PySide2.QtGui import QKeyEvent, QKeySequence
from PySide2.QtWidgets import QLineEdit, QLabel, QHBoxLayout
from widgets.widgets.extended.base.baseextendedwidget import BaseExtendedWidget


class PMGKeyMapCtrl(BaseExtendedWidget):
    def __init__(self, layout_dir: str, title: str, initial_value: str):
        super().__init__(layout_dir)
        self.on_check_callback = None
        # self.modifiers = {Qt.ControlModifier: Qt.CTRL, Qt.AltModifier: Qt.ALT, Qt.ShiftModifier: Qt.SHIFT,
        #                   Qt.AltModifier | Qt.ControlModifier: Qt.ALT + Qt.CTRL,
        #                   Qt.ControlModifier | Qt.ShiftModifier: Qt.SHIFT + Qt.CTRL
        #                   }
        self.modifiers = {}
        self.prefix = QLabel(text=title)

        entryLayout = QHBoxLayout()
        entryLayout.setContentsMargins(0, 0, 0, 0)
        self.ctrl = QLineEdit()
        self.ctrl.keyPressEvent = self.key_press
        # self.ctrl.textChanged.connect(self.ontext)

        self.central_layout.addWidget(self.prefix)
        self.central_layout.addLayout(entryLayout)
        entryLayout.addWidget(self.ctrl)
        self.set_value(initial_value)

    def key_press(self, event: QKeyEvent):
        k = self.modifiers.get(event.modifiers())
        if k is not None:
            key_seq = QKeySequence(k + event.key())
            try:
                text = key_seq.toString()
                self.ctrl.setText(text)
            except:
                import traceback
                traceback.print_exc()

    def set_value(self, value: str):
        # key_seq = QKeySequence(value)
        # key_seq.keyBindings()
        self.ctrl.setText(value)

    def get_value(self):
        return self.ctrl.text()
