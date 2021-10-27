import os
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QLocale, QTranslator

def create_translation(target_files: str):
    import os
    folder = os.path.dirname(target_files)
    name = os.path.basename(target_files)
    name_without_ext = os.path.splitext(name)
    names = ''
    for file_path in target_files:
        name = os.path.basename(file_path)
        names += name + ' '
    os.system('cd %s && pylupdate5 -noobsolete %s -ts translations/%s.ts' % (folder, names, name_without_ext))

def create_translator(path:str):

    inner_app = QApplication.instance()
    translator = QTranslator()
    translator.load(path)
    inner_app.installTranslator(translator)
    return translator