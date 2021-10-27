"""
fileutil定义的是文件输入输出的操作。
variableutils中定义的是将变量从文件加载或者将变量保存为文件的方法。
"""

from .variableutils import *
from .encoding import file_encoding_convert, file_encoding_detect
from .compressutils import make_targz_one_by_one, make_zip, unzip_file
from .search_in_path import search_in_path

