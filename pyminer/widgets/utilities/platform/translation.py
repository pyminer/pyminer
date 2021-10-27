def add_translation_file(file_path: str):
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import QTranslator
    app = QApplication.instance()
    if hasattr(app, 'trans'):
        try:
            tr = QTranslator()
            path = file_path
            tr.load(path)
            app.installTranslator(tr)
        except:
            pass
