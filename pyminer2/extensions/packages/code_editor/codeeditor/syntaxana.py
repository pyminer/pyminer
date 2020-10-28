import re

camelCaseRegex = re.compile(r'[\w|\d]([A-Z])')  # 识别驼峰命名的正则表达式
underLineCaseRegex = re.compile(r'_(\w)')  # 识别下划线命名方法的正则表达式


def find_camelcase_hint(word):
    sub = re.findall(camelCaseRegex, word)
    s = word[0] + ''.join(sub)
    return s


def find_underline_hint(word):
    sub = re.findall(underLineCaseRegex, word)
    s = word[0] + ''.join(sub)
    return s


def ifMatchCamelCase(word='', hint=''):
    """
    匹配形如‘isValidStudentNumber’这类的驼峰命名法。
    """
    global camelCaseRegex
    if len(word) >= 1:
        sub = re.findall(camelCaseRegex, word)

        s = word[0] + ''.join(sub)
        if s.lower().startswith(hint):
            return True
    return False


def ifMatchUnderlineCase(word='', hint=''):
    """
    匹配形如‘is_valid_student_number’这类的下划线命名法。
    """
    global underLineCaseRegex
    if len(word) >= 1:
        sub = re.findall(underLineCaseRegex, word)
        s = word[0] + ''.join(sub)
        if s.lower().startswith(hint):
            return True
    return False


def filter_words(word_list, hint):
    """
    提取下划线或者驼峰命名的字符。
    """
    result_list = []
    for word in word_list:
        if word.lower().startswith(hint):
            result_list.append(word)
        elif ifMatchCamelCase(word, hint):
            result_list.append(word)
            result_list.append(hint)
        elif ifMatchUnderlineCase(word, hint):
            result_list.append(word)
            result_list.append(hint)
        else:
            continue
    result_list = list(set(result_list))
    for i in range(len(result_list)):
        result_list[i] = result_list[i].strip() + ' '
    return result_list


if __name__ == '__main__':
    sub = re.findall(camelCaseRegex, 'CcAsDs')
    print(sub)
