import os
from typing import List, Tuple

import chardet
import re

ALL_SYMBOLS = '+.-*/(){}[]:;\"\'?><=%&|'
ALL_SYMBOLS_REGEX = r'[+\-\*/(){}\[\]:.;\"\'?><=%&| \t\n\r]'


def word_in_line(word: str, line: str, match_word: bool, match_case: bool) -> bool:
    if match_case:
        words = re.split(ALL_SYMBOLS_REGEX, line)
        if match_word:
            for w in words:
                if w == word:
                    return True
            return False
        else:
            return line.find(word) != -1
    else:
        word = word.lower()
        if match_word:
            words = re.split(ALL_SYMBOLS_REGEX, line)
            for w in words:
                if w.lower() == word:
                    return True
            return False
        else:
            return line.lower().find(word) != -1


def search_in_path(string_to_search: str, path: str, match_case: bool = False, match_word: bool = False,
                   file_exts: list = None) -> List[Tuple[int, str, str]]:
    """

    :param string_to_search:
    :param path:
    :param match_case:
    :param match_word:
    :param file_exts:
    :return: [行号，该行内容，文件名]
    """
    if file_exts is None:
        file_exts = ['.py', '.pyx', '.c', '.cpp', '.sql', '.html']
    file_exts_set = set(file_exts)
    ret = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext in file_exts_set:
                file_abso_path = os.path.join(dirpath, filename)
                with open(file_abso_path, 'rb') as f:
                    b = f.read()
                    det = chardet.detect(b)['encoding']
                    print(filename)
                    if det is None:
                        det = 'utf8'
                    s = b.decode(det, errors='replace')

                    s = s.replace('\r\n', '\n')
                    lines = s.split('\n')
                    for line_no, line in enumerate(lines):
                        if word_in_line(word=string_to_search, line=line, match_word=match_word, match_case=match_case):
                            ret.append((line_no, line, os.path.join(dirpath, filename)))
    return ret


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    res = search_in_path('print', path)
    print(res)
    # s = re.split(ALL_SYMBOLS_REGEX, 'if a==123:print(345)')
    # print(s)
