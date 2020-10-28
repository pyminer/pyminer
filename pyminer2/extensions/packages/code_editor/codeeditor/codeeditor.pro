SOURCES         = baseeditor.py \
                  tabwidget.py \
                  cppeditor.py \
                  cythoneditor.py \
                  pythoneditor.py \
                  syntaxana.py \
                  ui/ui_formeditor.py \
                  ui/ui_gotoline.py

FORMS           = ui/formeditor.ui \
                  ui/gotoline.ui

TRANSLATIONS    = translations/codeeditor_en.ts \
                  translations/codeeditor_zh_CN.ts \
                  translations/codeeditor_zh_TW.ts

CODECFORTR      = UTF-8
CODECFORSRC     = UTF-8

# pylupdate5.exe codeeditor.pro
# linguist.exe translations\codeeditor_en.ts translations\codeeditor_zh_CN.ts translations\codeeditor_zh_TW.ts