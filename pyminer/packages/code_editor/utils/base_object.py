from functools import cached_property
from pathlib import Path
from typing import Optional, Callable, TYPE_CHECKING

from PySide2.QtCore import QTranslator, QLocale
from PySide2.QtWidgets import QMessageBox

from lib.extensions.extensionlib import extension_lib
from ..settings import Settings

if TYPE_CHECKING:
    from lib.extensions.extensionlib.extension_lib import ExtensionLib
    from ...ipython_console.main import ConsoleInterface
    from ...applications_toolbar.main import ApplicationsInterface
    from ...embedded_browser.main import Interface as EmbeddedBrowserInterface
    from ...file_tree.main import Interface as FileTreeInterface


def _get_translator() -> Optional[QTranslator]:
    result = QTranslator()
    language = QLocale.system().name()
    file = Path(__file__).parent.parent / 'assets' / 'languages' / f'{language}.qm'
    if file.exists():
        result.load(str(file))
        return result
    else:
        return None


class CodeEditorBaseObject:
    # 由于插件内为独立的模块加载，其命名空间不共享，因此暂时只能采用这种方式实现全局的extension_lib读取
    extension_lib: 'ExtensionLib' = extension_lib
    settings = Settings()

    __translator = _get_translator()

    @cached_property
    def tr(self) -> Callable[[str], str]:
        """使用属性的方式返回一个运行时生成的函数。

        这个函数可以实现自动判断Context以查找对应的翻译。
        这个函数旨在解决的问题是，PySide2默认情况下采用静态编码的方式生成翻译，而后Python在运行时由于继承，类名不再是self.tr所在的类名，
        因此translator无法找到相对应的翻译。

        使用cached property以实现MRO查找等性能的节省。
        """
        klass_names = [klass.__name__ for klass in self.__class__.mro()]
        if self.__translator is None:
            return lambda source: source
        else:
            translate: Callable[[str, str], str] = self.__translator.translate

            def wrapper(source: str):
                translations = [translate(klass, source) for klass in klass_names]
                translations = [t for t in translations if t]
                return translations[0] if translations else source

            return wrapper

    def _not_implemented_error(self, name):
        title = self.tr('Not Implemented Error')
        message = self.tr('{} is not implemented').format(name)
        QMessageBox.critical(None, title, message)

    class __Interfaces:
        @cached_property
        def ipython_console(self) -> 'ConsoleInterface':
            return CodeEditorBaseObject.extension_lib.get_interface('ipython_console')

        @cached_property
        def application_toolbar(self) -> 'ApplicationsInterface':
            return CodeEditorBaseObject.extension_lib.get_interface('applications_toolbar')

        @cached_property
        def embedded_browser(self) -> 'EmbeddedBrowserInterface':
            return CodeEditorBaseObject.extension_lib.get_interface('embedded_browser')

        @cached_property
        def file_tree(self) -> 'FileTreeInterface':
            return CodeEditorBaseObject.extension_lib.get_interface('file_tree')

    interfaces: __Interfaces = __Interfaces()
