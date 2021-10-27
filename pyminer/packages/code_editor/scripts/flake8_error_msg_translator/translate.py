"""
将translations.txt转换为flake8_trans.json，以供PyMiner使用。
"""

import json
import re
from pathlib import Path
from pprint import pprint


def main():
    data = {}
    src = Path(__file__).parent.absolute() / 'translations.txt'
    dst = Path(__file__).parent.parent.parent.absolute() / 'assets' / 'flake8_trans.json'
    with open(src, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.replace('\n', '') for line in lines]
    lines = [line for line in lines if line.startswith(('E', 'W', 'C', 'F'))]
    lines = [list(line.strip().split(maxsplit=1)) for line in lines]
    lines = [[word.strip() for word in words] for words in lines if len(words) >= 1]
    [words.append('') for words in lines if len(words) == 1]
    lines = [(id, re.sub(' +', ' ', message)) for id, message in lines]
    [data.__setitem__(id, message) for id, message in lines]
    pprint(data)
    with open(dst, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    main()
