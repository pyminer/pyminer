import os
import shutil
import sys

# 文档的生程流程如下所示：
# 首先，根据*.py文件生成一系列的*.rst文件，然后根据*.rst文件生成html文件，即静态页面。

# 是否将文件上传
# 在进行页面上传时，会开启所有的强制刷新选项，这会降低页面的生成性能，但无伤大雅。
upload = False
# upload = True

# 项目的根路径，即pyminer项目的根文件夹
base = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, base)

# *.py文件夹，在这些路径读取*.py，然后生成*.rst文件
alg_src_dir = os.path.join(base, 'pyminer_algorithms')

# 用于存储rst模板的文件夹，这些模板用于生成*.rst文件
template_dir = os.path.join(base, 'docs', 'templates', 'apidoc')

# 根据*.py生成的*.rst文件夹
alg_rst_dir = os.path.join(base, 'docs', 'source', 'alg')
upload and os.path.exists(alg_rst_dir) and shutil.rmtree(alg_rst_dir)

# make文件的路径，本脚本调用sphinx的makefile实现功能
# TODO 目前仅支持调用windows下的makefile，请linux用户自行优化脚本并提交
make_path = os.path.join(base, 'docs', 'make.bat')

# 最终生成的html文件夹
html_path = os.path.join(base, 'docs', 'build', 'html')


def cmd(command):
    for line in os.popen(command):
        print(line, end='')


# 在上传时，强制重新生成*.rst文件，否则可以根据缓存加速rst文件生成过程
if upload:
    cmd(f'sphinx-apidoc -fMeo "{alg_rst_dir}" "{alg_src_dir}" -t {template_dir}')
else:
    cmd(f'sphinx-apidoc -Meo "{alg_rst_dir}" "{alg_src_dir}" -t {template_dir}')

# 在上传时，删除已有的html页面，并重新生成，否则可以利用缓存加速html生成过程
if upload:
    cmd(f'"{make_path}" clean')
cmd(f'"{make_path}" html')

# 进行单元测试
cmd(f'"{make_path}" doctest')

# 在上传时，将生成的html文件推送至gitee的pages仓库
if upload:
    cmd(f'ghp-import -npfr git@gitee.com:py2cn/pyminer -b pages "{html_path}"')
