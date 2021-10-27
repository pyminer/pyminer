def args_to_command(func_name, args: list, kwargs: dict):
    """
    将函数的参数和函数等转换为命令，方便IPython调用。
    注意：对于含有转义字符的场合，如'\n'，需要输入为'\\n'
    Args:
        func_name:
        args:
        kwargs:

    Returns:

    """
    args_str = ''
    for arg in args:
        args_str += repr(arg) + ','
    for k, v in kwargs.items():
        args_str += k + '=' + repr(v) + ','
    args_str = args_str.rstrip(',')
    return func_name + '(%s)' % args_str  # args,kwargs)


if __name__ == '__main__':
    cmd = args_to_command('pd.read_csv', [r'c:\users\aaa\desktop\test.csv'],
                          {'sep': ',', 'engine': 'c', 'nrows': 100})
    # 返回结果：pd.read_csv('c:\\users\\aaa\\desktop\\test.csv',sep=',',engine='c',nrows=100)
    # 相当于直接调用了相应的函数。
    print(cmd)
