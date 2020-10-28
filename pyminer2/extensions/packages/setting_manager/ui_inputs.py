from PyQt5.QtWidgets import QWidget,QLineEdit,QHBoxLayout,QVBoxLayout,QCheckBox,QComboBox,QSpinBox,QDoubleSpinBox,QLabel
class IntInput(QWidget):
    def __init__(self,parent,config):
        super().__init__(parent)
        self.hbox=QHBoxLayout(self)
        self.label=QLabel(self)
        self.label.setText(config.get("label","")+":")
        self.spin=QSpinBox(self)
        self.name=config['name']
        if maximum:=config.get('maximum'):
            self.spin.setMaximum(maximum)
        if minimum:=config.get('minimum'):
            self.spin.setMinimum(minimum)
        if default:=config.get('default'):
            self.spin.setValue(default)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.spin)
        self.setLayout(self.hbox)
    @property
    def value(self):
        return self.spin.value()
class DoubleInput(QWidget):
    def __init__(self,parent,config):
        super().__init__(parent)
        self.hbox=QHBoxLayout(self)
        self.label=QLabel(self)
        self.label.setText(config.get("label","")+":")
        self.spin=QDoubleSpinBox(self)
        self.name=config['name']
        if maximum:=config.get('maximum'):
            self.spin.setMaximum(maximum)
        if minimum:=config.get('minimum'):
            self.spin.setMinimum(minimum)
        if default:=config.get('default'):
            self.spin.setValue(default)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.spin)
        self.setLayout(self.hbox)
    @property
    def value(self):
        return self.spin.value()
class StrInput(QWidget):
    def __init__(self,parent,config):
        super().__init__(parent)
        self.hbox=QHBoxLayout(self)
        self.label=QLabel(self)
        self.label.setText(config.get("label","")+":")
        self.input=QLineEdit(self)
        self.name=config['name']
        if maxlen:=config.get('maxlen'):
            self.input.setMaxLength(maxlen)
        if place_holder:=config.get('place_holder'):
            self.input.setPlaceholderText(place_holder)
        if default:=config.get('default'):
            self.input.setText(default)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.input)
        self.setLayout(self.hbox)
    @property
    def value(self):
        return self.input.text()
class BoolInput(QWidget):
    def __init__(self,parent,config):
        super().__init__(parent)
        self.hbox=QHBoxLayout(self)
        self.label=QLabel(self)
        self.label.setText(config.get("label","")+":")
        self.checkbox=QCheckBox(self)
        self.name=config['name']
        if default:=config.get('default'):
            self.checkbox.setChecked(default)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.checkbox)
        self.setLayout(self.hbox)
    @property
    def value(self):
        return self.checkbox.isChecked()
class ComboInput(QWidget):
    def __init__(self,parent,config):
        super().__init__(parent)
        self.hbox=QHBoxLayout(self)
        self.label=QLabel(self)
        self.label.setText(config.get("label","")+":")
        self.combobox=QComboBox(self)
        self.combobox.addItems(config['items'])
        self.name=config['name']
        if default:=config.get('default'):
            self.combobox.setCurrentIndex(default)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.combobox)
        self.setLayout(self.hbox)
    @property
    def value(self):
        return self.combobox.currentText

inputs={
    'int':IntInput,
    'double':DoubleInput,
    'str':StrInput,
    'bool':BoolInput,
    'combo':ComboInput
}