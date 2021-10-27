SOURCES         = app2.py \
                  pyminer.py \
                  pmgui.py \
                  lib/check_dependency.py \
                  lib/base.py\


FORMS           = lib/ui/base/aboutMe.ui \
                  lib/ui/base/first_form.ui\
                  lib/ui/base/option.ui \
                  lib/ui/base/project_wizard.ui\
                  lib/ui/base/pm_marketplace/main.ui\
                  lib/ui/base/pm_marketplace/install.ui\
                  lib/ui/base/pm_marketplace/uninstall.ui\
                  lib/ui/base/pm_marketplace/package_manager_main.ui\

TRANSLATIONS    = languages/en/en.ts \
                  languages/zh_CN/zh_CN.ts \
                  languages/zh_TW/zh_TW.ts\

CODECFORTR      = UTF-8
CODECFORSRC     = UTF-8

# pylupdate5.exe pyminer.pro
# linguist.exe languages\en\en.ts languages\zh_CN\zh_CN.ts languages\zh_TW\zh_TW.ts