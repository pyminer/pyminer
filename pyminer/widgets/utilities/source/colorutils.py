def convert(c):
    v = ord(c)
    if (48 <= v <= 57):
        return v - 48
    else:
        return v - 87  # 返回a的值。


def color_str2tup(value: str) -> tuple:
    """
    pos或者wh的输入都是tuple
    """
    value = value.lower()
    c0 = convert(value[1])
    c1 = convert(value[2])
    c2 = convert(value[3])
    c3 = convert(value[4])
    c4 = convert(value[5])
    c5 = convert(value[6])
    a1 = c0 * 16 + c1
    a2 = c2 * 16 + c3
    a3 = c4 * 16 + c5
    return (a1, a2, a3)


def color_tup2str(value: tuple) -> str:
    """
    问题修正
    :param value:
    :return:
    """
    if value is None:
        return None
    strcolor = '#'
    for i in value:
        strcolor += hex(int(i))[-2:].replace('x', '0')
    return strcolor


if __name__ == '__main__':
    print(color_tup2str((0, 222, 155)))
    print(color_str2tup('#00aaff'))
