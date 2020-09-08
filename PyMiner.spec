# -*- mode: python ; coding: utf-8 -*-
import sys
import os


sys.setrecursionlimit(5000)
block_cipher = None
SETUP_DIR = os.getcwd()
files = ['app2.py']
pathex = os.getcwd()
datas = []


def get_file(root, suffix=''):
    files = os.listdir(root)
    result = []
    # prefix = set()
    for i in range(len(files)):
        path = os.path.join(root, files[i])
        if os.path.isdir(path):
            result.extend(get_file(path, suffix))
        if os.path.isfile(path) and path.endswith(suffix):
            if suffix == '.py' and 'app2.py' in path:
                pass
            else:
                result.append(path)
            # prefix.add('.' + path.split('.')[-1])
    return result


def get_suffix():
    files = get_file(os.getcwd())
    suffix = set()
    for file in files:
        suffix.add('.' + file.split('.')[-1])
    suffix = list(suffix)

    for sf in suffix:
        if '/' in sf:
            suffix.remove(sf)
    rev = ['.spec', '.gitignore', '.ui', '.md', '.txt', '.py']

    for i in rev:
        if i in suffix:
            suffix.remove(i)
    return suffix


def get_datas():
    datas = []
    suffix = get_suffix()
    root = os.getcwd()
    for sf in suffix:
        files = get_file(root, suffix=sf)
        for file in files:
            abs_file = os.path.split(file)[-1]
            datas.append((SETUP_DIR + file.replace(SETUP_DIR, ''), abs_file))
    return datas


files.extend(get_file(pathex, '.py'))
datas.extend(get_datas())

a = Analysis(files,
             pathex=pathex,
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PyMiner',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PyMiner')
