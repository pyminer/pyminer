"""
这个脚本用于制作PyMiner的安装包。
"""
import os
import shutil


def make_pyminer_installer():
    DIST_PATH = r"C:\Users\12957\Desktop\pyminer_dist\dist2"
    CONDA_PATH = r"C:\Users\12957\Desktop\pyminer_dist\Miniconda3-latest-Windows-x86_64.exe"
    CODE_FOLDER = os.path.join(DIST_PATH, "bin")
    ADDR = "https://gitee.com/py2cn/pyminer.git"
    BRANCH = "master"
    PACKUP_COMPONENTS_FOLDER = r"C:\Users\12957\Desktop\pyminer_dist\PyMiner打包组件"
    # os.system("start /wait "f" {CONDA_PATH} /InstallationType=JustMe /RegisterPython=0 /S /D={DIST_PATH}")
    if not os.path.exists(CODE_FOLDER):
        pass
    else:
        shutil.rmtree(CODE_FOLDER)

    # os.mkdir(CODE_FOLDER)
    os.system(f"git clone {ADDR} -b {BRANCH} {CODE_FOLDER}")
    for d in os.listdir(PACKUP_COMPONENTS_FOLDER):
        src = os.path.join(PACKUP_COMPONENTS_FOLDER, d)
        dest = os.path.join(DIST_PATH, d)
        shutil.copy(src, dest)

    PYTHON_PATH = os.path.join(DIST_PATH, "python.exe")
    os.system(f"{PYTHON_PATH} -m pip install -r  {os.path.join(CODE_FOLDER, 'requirements.txt')} -i "
              f"https://mirrors.cloud.tencent.com/pypi/simple")


if __name__ == '__main__':
    make_pyminer_installer()
