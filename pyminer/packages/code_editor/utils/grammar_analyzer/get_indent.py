from typing import Tuple


def get_indent(s: str) -> Tuple[str, int]:
    s = s.replace('\t', '    ')  # tab替换成四个空格
    s = s.rstrip()
    if len(s) > 0:
        for i, ch in enumerate(s):
            if ch != ' ':
                return s[i:], i
        return "", i + 1
    else:
        return "", 0
