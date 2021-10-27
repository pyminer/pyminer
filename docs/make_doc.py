import os
import sys
from os import path

base_path = path.abspath(path.join(__file__, '../..'))
sys.path.insert(0, base_path)

from sphinx.application import Sphinx

from pyminer_devutils.doc import RstGenerator, PythonFileTreeNode


def main():
    # 在这个文件下定义了文档的具体生成细节，包括rst文件夹的位置、排除的文档等。
    base = os.path.dirname(os.path.dirname(__file__))

    source_dir = path.join(base, 'docs', 'source')
    rst_root_dir = path.join(base, 'docs', 'build', 'rst')
    path.exists(rst_root_dir) or os.makedirs(rst_root_dir)

    generator = RstGenerator()

    generator.sync_directory(source_dir, rst_root_dir, rm=False)

    # 生成算法部分的文档
    py_dir = os.path.join(base, 'pyminer_algorithms')  # py源文件的目录
    rst_dir = os.path.join(rst_root_dir, 'alg')  # 根据py生成的rst文件的目录
    exclude_dir = [os.path.join(py_dir, p) for p in (
        # TODO (panhaoyu) 以下内容为无法自动生成的部分，请各位开发者自行检查其中的问题
        'plotting/graph.py',
    )]
    node = PythonFileTreeNode(py_dir, exclude_dir)
    generator.generate_python_package_files(node, rst_dir, 'pyminer_algorithms')

    # 生成界面部分的文档
    py_dir = os.path.join(base, 'pmgwidgets')  # py源文件的目录
    rst_dir = os.path.join(rst_root_dir, 'pmg')  # 根据py生成的rst文件的目录
    exclude_dir = [os.path.join(py_dir, p) for p in (
        # TODO (panhaoyu) 以下内容为无法自动生成的部分，请各位开发者自行检查其中的问题
        'display/browser/get_ipy.py',
        'widgets/basic/texts/webeditors/__init__.py',
        'examples',
        'display/browser/handler.py',
        'widgets/basic/quick/demo1.py',
        'widgets/basic/texts',
        'widgets/extended/texts/texteditor.py',
        'utilities/platform/test',
    )]
    node = PythonFileTreeNode(py_dir, exclude_dir)
    generator.generate_python_package_files(node, rst_dir, 'pmgwidgets')

    # 生成主程序的文档
    py_dir = os.path.join(base, 'pyminer2')  # py源文件的目录
    rst_dir = os.path.join(rst_root_dir, 'pyminer')  # 根据py生成的rst文件的目录
    exclude_dir = [os.path.join(py_dir, p) for p in (
        'extensions/packages',  # 插件文档独立生成，这里跳过。

        # TODO (panhaoyu) 以下内容为无法自动生成的部分，请各位开发者自行检查其中的问题
        'ui/pyqtsource_rc.py',
        'ui/base/widgets/resources.py',
        'core',
        'extensions/package_manager/package_manager.py',
        'features/io/database.py',
    )]
    node = PythonFileTreeNode(py_dir, exclude_dir)
    generator.generate_python_package_files(node, rst_dir, 'pyminer2')

    # 生成插件的文档
    py_dir = os.path.join(base, 'pyminer2/extensions/packages')  # py源文件的目录
    rst_dir = os.path.join(rst_root_dir, 'pkgs')  # 根据py生成的rst文件的目录
    exclude_dir = [os.path.join(py_dir, p) for p in (
        'ipython_console/initialize.py',  # IPython控制台的全局文件，没什么生成文档的意义，跳过

        # TODO (panhaoyu) 以下内容为无法自动生成的部分，请各位开发者自行检查其中的问题
        'pm_preprocess/ui/pyqtsource_rc.py',
        'code_editor',
        'data_miner',
        'cftool',
        'extension_app_demo',
        'pm_preprocess',
    )]
    node = PythonFileTreeNode(py_dir, exclude_dir)
    generator.generate_python_package_files(node, rst_dir, 'packages')

    # 生成开发工具文档
    py_dir = os.path.join(base, 'pyminer_devutils')  # py源文件的目录
    rst_dir = os.path.join(rst_root_dir, 'dev')  # 根据py生成的rst文件的目录
    exclude_dir = [os.path.join(py_dir, p) for p in tuple()]
    node = PythonFileTreeNode(py_dir, exclude_dir)
    generator.generate_python_package_files(node, rst_dir, 'pyminer_devutils')

    print('RST文件结构已生成。')

    app = Sphinx(
        srcdir=rst_root_dir,
        confdir=rst_root_dir,
        outdir=path.join(path.dirname(__file__), 'build/html'),
        doctreedir=path.join(path.dirname(__file__), 'build/doctrees'),
        buildername='html',
        confoverrides=dict(),
        status=sys.stdout,
        warning=sys.stderr,
        freshenv=False,
        warningiserror=False,
        tags=[],
        verbosity=0,
        parallel=0,
        # parallel=multiprocessing.cpu_count(),
        keep_going=True)
    app.build()


if __name__ == '__main__':
    main()
