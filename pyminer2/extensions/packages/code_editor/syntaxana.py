# -*- coding: utf-8 -*-
"""
powered by NovalIDE
来自NovalIDE的词法分析模块
作者：侯展意
词法分析模块的重要组成单元、
依靠各种正则表达式进行特征的提取。

"""
from typing import List, Tuple, Dict
import re


def getReplacingDic() -> Dict:
    dic = {'，': ',', '。': '.', '；': ';', '：': ':', '‘': '\'', '’': '\'', '“': '\"', '”': '\"', '【': '[', '】': ']',
           '（': '(', '）': ')'}
    return dic


def getIndent(s: str) -> Tuple[str, int]:
    s = s.replace('\t', '    ')  # tab替换成四个空格
    s = s.rstrip()
    if len(s) > 0:
        for i, ch in enumerate(s):
            if ch != ' ':
                return s[i:], i
        return "", i + 1
    else:
        return "", 0


def removeComment(s: str) -> str:
    pos = s.find('#')
    if pos != -1:
        return s[:pos]
    else:
        return s


def getStringContent(row):
    pass


def removeStringContent(row: str) -> str:
    row = row.replace('\"', '\'')
    if row.count('\'') >= 2:
        s = getAllFromRegex(regex=r'[\'](.*?)[\']', st=row)
        for item in s:
            row = row.replace('\'%s\'' % item, '\'\'')  # 带着分号一起换掉。
        return row
    else:
        return row


def parseVarType(row: str):
    getInfoFromRegex(r'[\'](.*?)[\']', row)


def getAllFromRegex(regex: str, st: str) -> List[str]:
    foundList = re.findall(re.compile(regex, re.S), st)

    return foundList


def getInfoFromRegex(regex: str, st: str) -> str:  # 从正则表达式中获取信息的函数。如果没有任何结果则返回0。
    foundList = re.findall(re.compile(regex, re.S), st)
    item = ''
    if foundList != []:
        item = foundList[0]
    return item


def getWordsFromString(s: str) -> list:
    if s != '':
        syms = s.split(',')  # 用逗号分隔开。
        for i in range(len(syms)):
            syms[i] = syms[i].strip()
        return syms
    else:
        return []


def countPar(row: str) -> Tuple[int, int, int]:  # 检测三类括号的数量。
    lparNum = row.count('(')
    rparNum = row.count(')')
    lbraceNum = row.count('{')
    rbraceNum = row.count('}')
    lbracketNum = row.count('[')
    rbracketNum = row.count(']')

    return lparNum - rparNum, lbraceNum - \
           rbraceNum, lbracketNum - rbracketNum  # 返回左括号数量减去右括号数量。


def checkPar(row: str) -> int:
    a, b, c = countPar(row)
    if (a == 0) & (b == 0) & (c == 0):
        return 1
    else:
        if (a < 0) | (b < 0) | (c < 0):
            return -1
        else:
            return 0


# 获取任何类型括号最外层内部的东西。（不是小括号！！！）
def getBracketedContent(row: str) -> Tuple[str, str, str]:
    # 返回值：一个表示括号类型的量，以及一个有关括号中内容的字符串，以及括号前的内容。
    lst = [-1, -1, -1]
    symList = ['(', '[', '{']
    symListCouple = [')', ']', '}']
    length = len(row)
    for i in range(len(lst)):
        lst[i] = row.find(symList[i])
        if lst[i] == -1:
            lst[i] = length
    minVal = min(lst)
    if minVal == length:  # 说明根本没括号
        return '', '', row[:minVal]  # 所以返回值不仅没有括号，还没有括号中的内容（废话）,只是返回括号前面的东西。
    else:
        pos = lst.index(minVal)  # 获取最小值的索引
        regex = r'[%s](.*)[%s]' % (symList[pos], symListCouple[pos])
        return symList[pos], getInfoFromRegex(
            regex=regex, st=row), row[:minVal]


def getFuncArgs(row: str) -> List[str]:  # 获取函数的输入参数。

    s = getInfoFromRegex(regex=r'[(](.*)[)]', st=row)

    li = getWordsFromString(s)

    if len(li) > 0:
        if li[0] == 'self':  # 不允许函数的第一个参数名字叫self。
            li.pop(0)
    for i in range(len(li)):
        eqSymPos = li[i].find('=')

        if eqSymPos != -1:  # 如果eqSymPos中有一个等号
            li[i] = li[i][:eqSymPos]  # 那么将等号去除
        colonSymPos = li[i].find(':')
        if colonSymPos != -1:
            li[i] = li[i][:colonSymPos]

    return li


def getFuncName(row: str) -> str:  # 获取函数的名称。
    return getInfoFromRegex(
        regex=r'def\s(.*?)[(]', st=row)  # 注意，需要匹配函数名，其中还有个空格。


def getLocalVarNames(row: str) -> List[str]:  # 获取局部变量的名称。
    li = getInfoFromRegex(regex=r'(.*?)[=]', st=row)  # 注意，需要匹配局部变量的名称，其中还有个空格。

    words = getWordsFromString(li)
    result = []
    for w in words:  # 如果是函数的方法，则不可。
        if w.find('.') == -1:
            result.append(w)
    return result


def is_number(str_number: str) -> bool:
    if (str_number.split(".")[0]).isdigit() or str_number.isdigit() or (str_number.split('-')[-1]).split(".")[
        -1].isdigit():
        return True
    else:
        return False


def getForVariables(row: str) -> List[int]:
    """
    获取for循环中定义的变量。
    """
    s = getInfoFromRegex(r'for(.*?)in', row)
    s = s.strip()
    return getWordsFromString(s)


def getVarType(row: str) -> str:
    """
    获取变量的类型，比如集合，数字等等。
    """
    bracket, content, outer = getBracketedContent(row)
    li = outer.split('=')
    if len(li) >= 1:

        if li[1].strip() == '':  # 这种情况下为直接赋值的语句，
            if bracket == '(':
                return ':tuple'
            elif bracket == '[':
                return ':list'
        else:
            st = li[1].split(',')[0]
            if is_number(st):
                return ':number'

    return ''


class Row():
    def __init__(self, pos: int, text: str, indent: int) -> None:
        self.pos = pos
        self.text = text
        self.indent = indent

    def __repr__(self) -> str:
        return 'row:' + repr(self.pos) + "\t indent:" + \
               repr(self.indent) + "\t text:" + self.text + '\n'


def regularize(rawText: List[str]) -> List[Row]:
    global kwdTuple, indexList, charStr

    f = rawText  # 获取打开的文件数组,每个元素是一行。
    regularifiedText = ''
    rowList = []
    currentRow = Row(0, '', 0)  # 创建一个没有含义的对象，这样方便类型检查。
    inStaticFunction = False
    inFunctionDefinition = False
    skipLine = False
    currentFuncIndent = 0
    currentIndent = 0
    funcIndent = 0

    for i, l in enumerate(f):
        line = removeStringContent(l)
        line = removeComment(line)

        if not skipLine:
            row, currentIndent = getIndent(line)  # 获取当前的行名和缩进，同时修剪掉行首的空格
            currentRow = Row(i, row, currentIndent)
            rowList.append(currentRow)

        else:
            currentRow.text += line.strip()  # 如果判断出这一行还没有结束，就不用获取当前的缩进，直接缀连即可。
            rowList.append(Row(i, '', 0))  # 这一行相应的没有任何内容

        cp = checkPar(currentRow.text)

        if cp == 0:  # 如果括号不匹配，那么就再继续进行,直至寻找到符合要求的行为止。
            skipLine = True
            if len(currentRow.text) >= 200:  # 长度超出，强行退出。
                skipLine = False
            continue
        elif cp == -1:  # 如果右边括号反倒更多,就跳出这种情况。
            skipLine = False
            continue
        else:
            skipLine = False
    return rowList


if __name__ == '__main__':
    regularize(['', '', ''])
