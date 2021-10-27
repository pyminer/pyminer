from PySide2.QtCore import Qt

from packages.code_editor.widgets.text_edit.python_text_edit import PMPythonCodeEdit


def test_get_selected_text(qtbot):
    window = PMPythonCodeEdit()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitForWindowShown(window)
    qtbot.wait(100)
    qtbot.keyClicks(window, 'a = 123')
    qtbot.keySequence(window, 'Ctrl+A')
    assert window.selected_code == 'a = 123'
    qtbot.keyClick(window, Qt.Key_Right)
    qtbot.keyClick(window, Qt.Key_Return)
    qtbot.keyClicks(window, 'print(123)')
    qtbot.keyClick(window, Qt.Key_Return)
    qtbot.keySequence(window, 'Shift+Up')
    assert window.selected_code == 'print(123)\n'
    qtbot.keyClick(window, Qt.Key_Right)
    qtbot.keyClick(window, Qt.Key_Right)
    qtbot.keyClick(window, Qt.Key_Right)
    assert window.selected_code == ''
    qtbot.keyClick(window, Qt.Key_Up)
    assert window.selected_code == 'print(123)'
