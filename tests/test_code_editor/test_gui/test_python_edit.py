from packages.code_editor.widgets.text_edit.python_text_edit import PMPythonCodeEdit


def test_myapp(qtbot):
    window = PMPythonCodeEdit()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitForWindowShown(window)
    qtbot.keyClicks(window, 'a=123')
    assert window.code == 'a=123'
