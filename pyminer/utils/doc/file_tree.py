import glob
from fnmatch import fnmatch
from functools import cached_property
from os import path
from typing import List


class FileTreeNode(object):
    """
    本类用于识别Python文件结构。

    获取文件树，并排除用户指定过滤的部分。

        关于文件结构的过滤功能都写在了这个文件夹里，包括以下内容：

        #. 对于非 ``python package`` 的部分全部跳过；
        #. 跳过由 ``.`` 和 ``_`` 开头的文件和文件夹，不过保留 ``__*__`` 格式的文件和文件夹；
        #. 跳过 ``__pycache__`` 文件夹；
        #. 跳过用户指定要排除的文件夹。
    """

    SUFFIXES = ('.py', '.pyx', '.pyw')
    CORE_NAME = '__init__'

    def __init__(self, directory: str, exclude: List[str]):
        """
        根据指定的模式对文件夹进行解析，其递归的结果就是文件树。

        将文件夹分为以下内容：

        ================ =================================== ======================
          类别             标准                                以Python为例的解释
        ================ =================================== ======================
          核心文件         后缀名为 ``.suffix`` 的文件         Python模块
          非核心文件       后缀名不为 ``.suffix`` 的文件       其他文件
          核心文件夹       包含 ``core.suffix`` 的文件夹       Python包
          非核心文件夹     不包含 ``core.suffix`` 的文件夹     其他文件夹
        ================ =================================== ======================

        这四部分将分别采用不同的方式进行处理。

        有一些额外的点需要说明，（这里仅以python文件结构为例）：

        #. __init__.py 将不会显示在核心文件和非核心文件中；

        Args:
            directory: 需要计算文件树的文件夹。
            exclude: 需要排除的模式，采用标准库的fnmatch进行匹配。

        Returns:
            整理后的文件树
        """
        self.directory = path.abspath(directory)
        self.exclude_patterns = exclude

    @cached_property
    def filtered_sub_paths(self):
        """定义基本的基于用户的 ``exclude`` 参数的过滤器"""
        result = glob.glob(path.join(self.directory, '*'))
        for file_path in result.copy():  # 这里要采用复制，因为遍历过程的原位删除会改变其遍历过程
            # 删去用户指定排除的文件和文件夹
            if any(fnmatch(file_path, pattern) for pattern in self.exclude_patterns):
                result.remove(file_path)
                continue
        # 由于其他的路径都是从这里导出的，在这里进行一次排序，别的位置就不需要排序了
        return sorted(result)

    @cached_property
    def sub_files(self) -> List[str]:
        """子文件的路径列表，包括核心文件、其他文件及索引文件。"""
        return [child for child in self.filtered_sub_paths if path.isfile(child)]

    @cached_property
    def sub_core_files(self) -> List[str]:
        """核心子文件的路径列表。"""
        # 判断后缀是否是核心文件的后缀
        result = [file for file in self.sub_files if path.splitext(file)[1] in self.SUFFIXES]
        # 判断基本名是否不是基本名
        result = [p for p in result if path.splitext(path.split(p)[1])[0] != self.CORE_NAME]
        return result

    @cached_property
    def sub_other_files(self):
        # 判断后缀是否是核心文件的后缀
        result = [file for file in self.sub_files if path.splitext(file)[1] not in self.SUFFIXES]
        # 判断基本名是否不是基本名
        result = [p for p in result if path.splitext(path.split(p)[1])[0] != self.CORE_NAME]
        return result

    @cached_property
    def sub_directories(self) -> List['FileTreeNode']:
        """子文件夹，包括核心文件夹和其他文件夹"""
        return [FileTreeNode(child, self.exclude_patterns) for child in self.filtered_sub_paths if path.isdir(child)]

    @cached_property
    def sub_core_directories(self) -> List['FileTreeNode']:
        """子包"""
        result = [node for node in self.sub_directories if node.is_core_directory]
        return result

    @cached_property
    def sub_other_directories(self) -> List['FileTreeNode']:
        """其他文件夹"""
        return [d for d in self.sub_directories if not d.is_core_directory]

    @cached_property
    def is_core_directory(self) -> bool:
        """是否是核心包"""
        # 取删去文件夹后的基本名
        sub_files = [path.split(file)[1] for file in self.sub_files]
        # 判断是否包含索引文件
        for suffix in self.SUFFIXES:
            if f'{self.CORE_NAME}{suffix}' in sub_files:
                return True
        return False


class PythonFileTreeNode(FileTreeNode):
    @cached_property
    def filtered_sub_paths(self):
        """定义针对Python的过滤器"""
        result = super(PythonFileTreeNode, self).filtered_sub_paths.copy()
        for file_path in result.copy():  # 这里要采用复制，因为遍历过程的原位删除会改变其遍历过程
            dir_name, file_name = path.split(file_path)
            base_name, ext_name = path.splitext(file_name)
            # 删去由 ``.`` 和 ``_`` 开头的文件和文件夹，不过对于 ``__*__`` 格式的不进行操作
            if base_name.startswith(('.', '_')) and not (base_name.startswith('__') and base_name.endswith('__')):
                result.remove(file_path)
                continue

            # 删去 ``__pycache__`` 文件夹
            if path.isdir(file_path) and base_name == '__pycache__':
                result.remove(file_path)
                continue
        return result


class RstFileTreeNode(FileTreeNode):
    """
    针对 `.rst` 文件结构的过滤器，用于对生成后的文档结构进行识别。

    主要是用于增量更新的过程中，需要判断哪些文件是无用的需要删除的。

    本类实现了对 ``.rst`` 文件结构的过滤，可以用于配合 ``PythonFileTreeNode`` 找出这些需要被删除的文件。
    
    这个类暂时没有派上用场。
    """
    SUFFIXES = ('.md', '.rst')
    CORE_NAME = 'index'
