"""
定义该插件下的一些常用变量及配置项，包括资源文件夹位置等内容。
"""

from pathlib import Path

from PySide2.QtGui import QIcon


class Settings:
    base_dir = Path(__file__).parent.absolute()
    assets_dir = base_dir / 'assets'
    icons_dir = assets_dir / 'icons'
    translations_dir = assets_dir / 'translations'

    def get_icon(self, name: str) -> QIcon:
        return QIcon(str(self.icons_dir / name))
