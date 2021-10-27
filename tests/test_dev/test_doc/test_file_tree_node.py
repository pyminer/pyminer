from os import path

from pyminer_devutils.doc.file_tree import FileTreeNode, PythonFileTreeNode


def test_file_tree_node():
    """测试基本的文件树节点"""
    base = path.abspath(path.join(__file__, '../test_case_for_file_tree_node'))
    node = FileTreeNode(base, [])
    assert node.sub_core_files == [path.join(base, p) for p in ('_exclude.py', 'main.py')]
    assert node.sub_other_files == [path.join(base, 'README.md')]
    assert [n.directory for n in node.sub_core_directories] == [path.join(base, p) for p in ('sub_dir', 'sub_dir2')]
    assert [n.directory for n in node.sub_other_directories] == [path.join(base, p) for p in ('sub_dir3',)]
    assert node.is_core_directory


def test_python_file_tree_node():
    """测试针对Python的文件树节点"""
    base = path.abspath(path.join(__file__, '../test_case_for_file_tree_node'))
    node = PythonFileTreeNode(base, [])
    assert node.sub_core_files == [path.join(base, p) for p in ('main.py',)]
    assert node.sub_other_files == [path.join(base, 'README.md')]
    assert [n.directory for n in node.sub_core_directories] == [path.join(base, p) for p in ('sub_dir', 'sub_dir2')]
    assert [n.directory for n in node.sub_other_directories] == [path.join(base, p) for p in ('sub_dir3',)]
    assert node.is_core_directory


def test_exclude():
    base = path.abspath(path.join(__file__, '../test_case_for_file_tree_node'))
    node = FileTreeNode(base, ['*/main.py'])
    assert node.sub_core_files == [path.join(base, p) for p in ('_exclude.py',)]
    assert node.sub_other_files == [path.join(base, 'README.md')]
    assert [n.directory for n in node.sub_core_directories] == [path.join(base, p) for p in ('sub_dir', 'sub_dir2')]
    assert [n.directory for n in node.sub_other_directories] == [path.join(base, p) for p in ('sub_dir3',)]
    assert node.is_core_directory
