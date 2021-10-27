from PySide2.QtCore import Qt

from packages.code_editor.widgets.editors.python_editor import PMPythonEditor


def test_format_code(qtbot):
    window = PMPythonEditor()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitForWindowShown(window)
    qtbot.wait(100)
    qtbot.keyClicks(window.text_edit, 'a  = 123')
    qtbot.keySequence(window.text_edit, 'Ctrl+Alt+F')
    assert window.text() == 'a = 123\n'


def test_auto_completion(qtbot):
    window = PMPythonEditor()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitForWindowShown(window)
    qtbot.keyClicks(window.text_edit, 'import num')
    qtbot.wait(1000)
    # TODO 这里的按键事件为何是传递到dropdown而非text_edit
    qtbot.keyClick(window.text_edit.autocompletion_dropdown, Qt.Key_Return)
    qtbot.wait(1000)
    assert window.text() == 'import numbers'


def test_format_when_editing(qtbot):
    """回车后会自动调整格式"""
    window = PMPythonEditor()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitForWindowShown(window)
    qtbot.wait(100)
    qtbot.keyClicks(window.text_edit, 'def a():')
    qtbot.keyClick(window.text_edit, Qt.Key_Return)
    qtbot.keyClicks(window.text_edit, 'print(123)')
    assert window.text_edit.code == 'def a():\n    print(123)'


def test_comment(qtbot):
    """注释功能和反注释功能"""
    window = PMPythonEditor()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitForWindowShown(window)
    qtbot.wait(100)
    window.text_edit.setPlainText('def a():\n    print(123)\n')
    qtbot.keySequence(window.text_edit, 'Ctrl+A')
    qtbot.keySequence(window.text_edit, 'Ctrl+/')
    assert window.text_edit.code == '#def a():\n#    print(123)\n#'
    qtbot.keySequence(window.text_edit, 'Ctrl+/')
    assert window.text_edit.code == 'def a():\n    print(123)\n'
    qtbot.keyClick(window.text_edit, Qt.Key_Left)
    qtbot.keySequence(window.text_edit, 'Ctrl+/')
    assert window.text_edit.code == '#def a():\n    print(123)\n'
    qtbot.keySequence(window.text_edit, 'Ctrl+/')
    assert window.text_edit.code == 'def a():\n    print(123)\n'
