from pmgwidgets import UndoManager


def test_push():
    manager = UndoManager()
    manager.push('a')
    manager.push('ab')
    manager.push('abc')
    manager.push('ab')
    manager.push('abd')
    manager.push('abde')
    manager.push('abdef')
    manager.push('abdefg')
    assert manager.content == ['a', 'ab', 'abc', 'ab', 'abd', 'abde', 'abdef', 'abdefg']
    assert manager.pointer == 7
    assert len(manager) == 8


def test_undo():
    manager = UndoManager()
    manager.push('a')
    manager.push('ab')
    manager.push('abc')
    manager.push('ab')
    assert manager.content == ['a', 'ab', 'abc', 'ab']
    assert manager.pointer == 3
    assert len(manager) == 4
    assert manager.undo() == 'ab'
    assert manager.pointer == 2
    # 撤销后不会改变长度
    assert len(manager) == 4


def test_redo():
    manager = UndoManager()
    manager.push('a')
    manager.push('ab')
    manager.push('abc')
    manager.push('ab')
    assert manager.content == ['a', 'ab', 'abc', 'ab']
    assert manager.undo() == 'ab'
    assert manager.undo() == 'abc'
    assert manager.redo() == 'abc'
    assert manager.redo() == 'ab'


def test_last_value():
    manager = UndoManager()
    manager.push('a')
    manager.push('ab')
    manager.push('abc')
    manager.push('ab')
    assert manager.content == ['a', 'ab', 'abc', 'ab']
    assert manager.last_value() == 'ab'
    assert manager.undo() == 'ab'
    assert manager.last_value() == 'abc'
    assert manager.undo() == 'abc'
    assert manager.last_value() == 'ab'
    assert manager.redo() == 'abc'
    assert manager.last_value() == 'abc'
    assert manager.redo() == 'ab'
    assert manager.last_value() == 'ab'
