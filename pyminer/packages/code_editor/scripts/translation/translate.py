import os
import sys
from pathlib import Path

import PySide2
import jinja2

sys.path.insert(1, str(Path(__file__).absolute().parent.parent.parent.parent.parent))

from utils.dev.system import system


def get_python_files():
    base_path = Path(__file__).parent.parent.parent.absolute()
    python_files = []
    for root, sub_dirs, files in os.walk(base_path):
        root = Path(root)
        if any(p in root.parts for p in ('__pycache__', 'assets', 'scripts')):
            continue
        for file in files:
            file = root / file
            if file.suffix != '.py':
                continue
            file = os.path.join('..', '..', file.relative_to(base_path))
            python_files.append(file)
    return python_files


def main():
    # 生成pro文件
    # TODO 由于目前没有ui文件，因此没有考虑ui文件
    template = Path(__file__).absolute().parent / 'code_editor.pro_t'
    with open(template, 'r', encoding='utf-8') as f:
        template_content = f.read()
    python_files = get_python_files()
    python_files = '\\\n                  '.join(python_files)
    pro_content = jinja2.Template(template_content).render(python_files=python_files)
    pro = Path(__file__).absolute().parent / 'code_editor.pro'
    with open(pro, 'w', encoding='utf-8') as f:
        f.write(pro_content)

    # 使用lupdate生成ts文件
    exe = Path(PySide2.__file__).parent / 'pyside2-lupdate.exe'
    system(exe, pro)

    # 将ts文件转换为qm文件
    base_path = Path(__file__).absolute().parent.parent.parent
    exe = Path(PySide2.__file__).parent / 'lrelease.exe'
    ts_dir = base_path / 'assets' / 'languages'
    for file in ts_dir.glob('*.ts'):
        output = file.parent / f'{file.stem}.qm'
        system(exe, f'{file}', '-qm', output)


if __name__ == '__main__':
    main()
