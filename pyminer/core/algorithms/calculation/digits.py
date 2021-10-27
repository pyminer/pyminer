"""
与数字进制转换有关的方法。
十进制小数转IEEE754标准的单精度浮点数。
贡献者：_Nigel_
https://blog.csdn.net/qq_40890756/article/details/83111431

"""


def ConvertFixedIntegerToComplement(fixedInterger):  # 浮点数整数部分转换成补码(整数全部为正)
    return bin(fixedInterger)[2:]


def ConvertFixedDecimalToComplement(fixedDecimal):  # 浮点数小数部分转换成补码
    fixedpoint = int(fixedDecimal) / (10.0 ** len(fixedDecimal))
    s = ''
    while fixedDecimal != 1.0 and len(s) < 23:
        fixedpoint = fixedpoint * 2.0
        s += str(fixedpoint)[0]
        fixedpoint = fixedpoint if str(fixedpoint)[0] == '0' else fixedpoint - 1.0
    return s


def ConvertToExponentMarker(number):
    """
    阶码生成
    """
    return bin(number + 127)[2:].zfill(8)


def ConvertToFloat(floatingPoint):
    """
    转换成IEEE754标准的数
    Args:
        floatingPoint:

    Returns:

    """
    floatingPointString = str(floatingPoint)
    if floatingPointString.find('-') != -1:  # 判断符号位
        sign = '1'
        floatingPointString = floatingPointString[1:]
    else:
        sign = '0'
    l = floatingPointString.split('.')  # 将整数和小数分离
    front = ConvertFixedIntegerToComplement(int(l[0]))  # 返回整数补码
    rear = ConvertFixedDecimalToComplement(l[1])  # 返回小数补码
    floatingPointString = front + '.' + rear  # 整合
    relativePos = floatingPointString.find('.') - floatingPointString.find('1')  # 获得字符1的开始位置
    if relativePos > 0:  # 若小数点在第一个1之后
        exponet = ConvertToExponentMarker(relativePos - 1)  # 获得阶码
        mantissa = floatingPointString[
                   floatingPointString.find('1') + 1: floatingPointString.find('.')] + floatingPointString[
                                                                                       floatingPointString.find(
                                                                                           '.') + 1:]  # 获得尾数
    else:
        exponet = ConvertToExponentMarker(relativePos)  # 获得阶码
        mantissa = floatingPointString[floatingPointString.find('1') + 1:]  # 获得尾数
    mantissa = mantissa[:23] + '0' * (23 - len(mantissa))
    floatingPointString = '0b' + sign + exponet + mantissa
    return hex(int(floatingPointString, 2))
