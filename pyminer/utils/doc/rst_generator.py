import os
import shutil
from fnmatch import fnmatch
from glob import glob
from os import path
from typing import List

from jinja2 import Environment, PackageLoader
from sphinx.util.osutil import FileAvoidWrite

from .file_tree import PythonFileTreeNode


class RstGenerator(object):
    """
    根据 ``python`` 文件结构生成 ``rst`` 文件结构。

    #. 对于不存在的文件，直接生成；
    #. 对于已存在的文件，判断是否更新，如果更新则覆写，否则不改变，以免触发 ``sphinx`` 的更新机制；
    #. 对于多余的文件，删除。

    本方法首先根据 ``python`` 文件结构生成 ``rst`` 文件结构，
    然后再将其余文件进行拷贝。
    因此，如果您本方法生成的 ``*.rst`` 不满意的话，可以采用与 ``python`` 文件同名但不同后缀的文件覆写自动生成的文件。

    Examples：

        .. code-block::

            package
              |- __init__.py
              |- __init__.rst

        则 ``__init__.py`` 的内容会被弃用，而 ``__init__.rst`` 的内容会被拷贝过去。

    Notes:
        本程序旨在对文档进行增量更新，目前的方案是整体删除然后再进行构建。
        这是一个非常低效的方案，应当判断是否需要更新，如果需要更新的话再进行重新复制。

        TODO (panhaoyu) 应删除多余的文件。


    """

    def __init__(self):
        self.env = Environment(loader=PackageLoader('pyminer_devutils', 'doc/template'))
        self.module_template = self.env.get_template('module.rst_t')
        self.package_template = self.env.get_template('package.rst_t')

    def generate_python_index_file(self, src_tree: PythonFileTreeNode, dst_dir: str, pkg_name: str) -> str:
        """根据Python的__init__.py生成包的索引文件

        # 将 ``__init__.py`` 进行单独处理
        # 区别于其他的模块， ``__init__.py`` 相当于是包的主页，因此采用了包的模板，而非模块的模板。

        Args:
            src_tree: 源文件夹的文件树节点。
            dst_dir: 目标文件夹路径，不包括 ``index.rst`` 文件名。
            pkg_name: 包名，用于进行 ``autodoc`` 的 ``import``。

        Returns:
            生成的文件的路径。
        """
        sub_packages = [path.split(node.directory)[1] for node in src_tree.sub_core_directories]
        sub_modules = [path.split(path.splitext(module)[0])[1] for module in src_tree.sub_core_files]
        dst = path.join(dst_dir, 'index.rst')
        content = self.package_template.render(
            pkgname=pkg_name, subpackages=sub_packages, submodules=sub_modules)
        with FileAvoidWrite(dst) as f:
            f.write(content)
        return dst

    def generate_python_module_files(self, src_tree: PythonFileTreeNode, dst_dir: str, pkg_name: str) -> List[str]:
        """生成一个目录下的所有python模块对应的rst文件。

        Args:
            src_tree: 源文件夹的文件树节点。
            dst_dir: 目标文件夹路径，不包括 ``index.rst`` 文件名。
            pkg_name: 包名，用于进行 ``autodoc`` 的 ``import``。

        Notes:
            这里不包括 ``__init__.py`` ，因为它们是单独生成的。

        Returns:
            生成的文件路径。
        """
        created_files = []
        for module in src_tree.sub_core_files:
            module = path.split(module)[1]
            module = path.splitext(module)[0]
            content = self.module_template.render(pkgname=f'{pkg_name}.{module}')
            dst_file = path.join(dst_dir, f'{module}.rst')
            with FileAvoidWrite(dst_file) as f:
                f.write(content)
                created_files.append(dst_file)
        return created_files

    def generate_asset_files(self, src_tree: PythonFileTreeNode, dst_dir: str) -> List[str]:
        """生成除了 ``*.py`` 文件之外的资源文件。

        这个函数只是对文件的简单拷贝。

        这里的拷贝采用的是 ``shutil.copy2`` 进行的，这个函数可以同时拷贝文件的时间戳等信息，
        这样可以避免触发 ``sphinx`` 由于文件更新导致的重编译。

        Args:
            src_tree: 源文件夹的文件树节点。
            dst_dir: 目标文件夹路径，不包括 ``index.rst`` 文件名。

        Returns:
            生成的文件路径。
        """
        created_files = []
        for file in src_tree.sub_other_files:
            dst_file = path.join(dst_dir, path.split(file)[1])
            self.copy_if_update(file, dst_file)
            created_files.append(dst_file)
        return created_files

    @staticmethod
    def copy_if_update(src: str, dst: str):
        """这个函数是对于 ``shutil.copy2`` 的封装，如果文件无变化则不复制。

        Args:
            src: 源文件。
            dst: 目标文件。
        """
        if not path.exists(dst):
            shutil.copy2(src, dst)
            return
        with open(src, mode='rb') as fsrc, open(dst, mode='rb') as fdst:
            content_src = fsrc.read()
            content_dst = fdst.read()
        if content_src != content_dst:
            shutil.copy2(src, dst)

    def sync_directory(self, src_dir: str, dst_dir: str, rm=True):
        """递归地同步一个文件夹。

        同步为完全同步，如有更新的文件则创建，如有多余的文件则删除。

        Args:
            src_dir: 源文件夹。
            dst_dir: 新文件夹。
            rm: 是否删除多余的文件及文件夹。
        """
        # 如果目标文件夹不存在，则简单复制就可以
        if not path.exists(dst_dir):
            shutil.copytree(src_dir, dst_dir)
            return

        # 如果目标不是一个文件夹，那将其进行删除并创建
        if not path.isdir(dst_dir):
            os.remove(dst_dir)
            shutil.copytree(src_dir, dst_dir)
            return

        # 删除多余的文件和文件夹
        src_sub_paths = glob(path.join(src_dir, '*'))
        src_sub_dirs = [p for p in src_sub_paths if path.isdir(p)]
        src_sub_files = [p for p in src_sub_paths if path.isfile(p)]
        src_sub_dir_names = [path.relpath(d, src_dir) for d in src_sub_dirs]
        src_sub_file_names = [path.relpath(p, src_dir) for p in src_sub_files]
        dst_sub_dirs = [path.join(dst_dir, name) for name in src_sub_dir_names]
        dst_sub_files = [path.join(dst_dir, name) for name in src_sub_file_names]
        if rm:
            for sub_path in glob(path.join(dst_dir, '*')):
                path.isdir(sub_path) and path not in dst_sub_dirs and shutil.rmtree(sub_path)
                path.isfile(sub_path) and path not in dst_sub_files and os.remove(sub_path)

        # 如果目标文件夹存在，递归判断是否复制。
        for src_sub_path in glob(path.join(src_dir, '*')):
            _, sub_name = path.split(src_sub_path)
            dst_sub_path = path.join(dst_dir, sub_name)
            if path.isdir(src_sub_path):
                self.sync_directory(src_sub_path, dst_sub_path)
            elif path.isfile(src_sub_path):
                self.copy_if_update(src_sub_path, dst_sub_path)

    def generate_asset_directoreis(self, src_tree: PythonFileTreeNode, dst_dir: str) -> List[str]:
        """生成除了 ``python package`` 文件夹之外的资源文件夹。

        这个函数只是对文件夹的简单拷贝。

        这里的拷贝采用的是 ``shutil.copy2`` 进行的，这个函数可以同时拷贝文件的时间戳等信息，
        这样可以避免触发 ``sphinx`` 由于文件更新导致的重编译。

        Args:
            src_tree: 源文件夹的文件树节点。
            dst_sub_dir: 目标文件夹路径，不包括 ``index.rst`` 文件名。

        Returns:
            生成的文件夹列表。
        """
        # 将所有的非 ``python package`` 的文件夹进行简单的拷贝
        created_dirs = []
        for node in src_tree.sub_other_directories:
            dst_sub_dir = path.join(dst_dir, path.relpath(node.directory, src_tree.directory))
            self.sync_directory(node.directory, dst_sub_dir)
            created_dirs.append(dst_sub_dir)
        return created_dirs

    def generate_python_package_files(self, tree: PythonFileTreeNode, dst_dir: str, pkg_name: str) -> str:
        """ 基于一个 ``python package`` 生成相应的文件夹。

        这个函数可以理解为是这个类的主函数，
        它将递归对子包进行生成。

        Args:
            tree: 源文件，是一个 ``Node`` 节点。
            dst_dir: 生成的 ``rst`` 文件结构。
            pkg_name: 用于写入模版中的 ``package_name`` 。

        Returns:
            暂无返回值

        Notes:
            本模块区别于 ``shpinx-apidoc`` 的将所有文件放在一个文件夹的方案，
            采用了层级的方案进行 ``rst`` 文件结构的组织。
            这样生成的内容更直观，且可以包含非 ``*.py`` 文件。

        Returns:
            创建的文件夹路径。
        """
        path.exists(dst_dir) or os.mkdir(dst_dir)
        dst_dir = path.abspath(dst_dir)

        # 生成所有的文件以及资源文件夹。
        # Python包直接递归调用自身。
        created_files: List[str] = []
        created_files.append(self.generate_python_index_file(tree, dst_dir, pkg_name))
        created_files.extend(self.generate_python_module_files(tree, dst_dir, pkg_name))
        created_files.extend(self.generate_asset_files(tree, dst_dir))

        create_dirs: List[str] = []
        create_dirs.extend(self.generate_asset_directoreis(tree, dst_dir))

        # 将所有的 ``sub_package`` 子包进行递归处理
        for package in tree.sub_core_directories:
            sub_package_name = path.split(package.directory)[1]
            package_name_to_render = f'{pkg_name}.{sub_package_name}'
            dst = path.join(dst_dir, sub_package_name)
            create_dirs.append(self.generate_python_package_files(package, dst, package_name_to_render))

        # 删去多余的文件及文件夹
        for sub_path in glob(path.join(dst_dir, '*')):
            path.isdir(sub_path) and not any(fnmatch(sub_path, d) for d in create_dirs) and shutil.rmtree(sub_path)
            path.isfile(sub_path) and not any(fnmatch(sub_path, f) for f in created_files) and os.remove(sub_path)

        return dst_dir
