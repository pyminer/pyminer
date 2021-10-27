import os
import sys
import chardet


def file_encoding_convert(input_file: str, input_encoding: str, output_file: str, output_encoding: str):
    """
    文件编码格式转换
    Args:
        input_file:输入文件绝对路径
        output_file: 输出文件绝对路径
        input_encoding: 输入文件编码方式，按照这个方式进行解码
        output_encoding: 输出文件编码方式

    Returns:

    """
    if not os.path.exists(input_file):
        raise FileNotFoundError('Input file %s not found!' % (input_file))
    with open(input_file, 'rb') as f:
        b = f.read()
    b1 = b.decode(input_encoding, 'ignore').encode(output_encoding, 'replace')
    with open(output_file, 'wb') as f:
        f.write(b1)


def file_encoding_detect(path: str, detect_len: int = 1000):
    """
    通过文件的开头若干字节检测文件的编码方式。
    Args:
        path:
        detect_len:

    Returns:

    """
    if not os.path.exists(path):
        raise FileNotFoundError('File not found:%s' % path)
    size = os.path.getsize(path)
    print(size)

    with open(path, 'rb') as f:
        if size > detect_len and detect_len > 0:
            b = f.read(detect_len)
        else:
            b = f.read()
            pass
    return chardet.detect(b)['encoding']


if __name__ == '__main__':
    utf8_file = os.path.join(os.path.dirname(__file__), 'source', 'encoding', 'test_utf8.csv')
    ascii_file = os.path.join(os.path.dirname(__file__), 'source', 'encoding', 'test_ascii.csv')
    gbk_file = os.path.join(os.path.dirname(__file__), 'source', 'encoding', 'test_gbk.csv')
    gb2312_file = os.path.join(os.path.dirname(__file__), 'source', 'encoding', 'test_gb2312.csv')
    file_encoding_convert(utf8_file, 'utf8', ascii_file, 'ascii')
    file_encoding_convert(utf8_file, 'utf8', gbk_file, 'gbk')
    file_encoding_convert(gbk_file, 'gbk', gb2312_file, 'gb2312')

    encoding = file_encoding_detect(utf8_file)
    print(encoding)
    encoding = file_encoding_detect(ascii_file, -1)
    print(encoding)
