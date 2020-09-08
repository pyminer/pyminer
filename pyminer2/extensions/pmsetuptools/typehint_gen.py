import os

def analyse_class(cls:type, path:str=os.path.dirname(__file__)):
    cls_name = cls.__name__
    base_name = cls.__base__.__name__
    file_name = cls_name.lower()+'.py'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file_name), 'w') as f:
        f.write(f'class {cls_name}({base_name}):\n\n')
        for attr in cls.__dict__:
            if attr.startswith('_'):
                continue
            val = getattr(cls, attr)
            if not callable(val):
                continue
            func_name = attr
            func = val
            argnames = list(func.__code__.co_varnames)
            argnames.pop(0)  # self
            args = [{'name': argname} for argname in argnames]
            pos_args_no = func.__code__.co_argcount - 1
            for i in range(pos_args_no):
                args[i]['type'] = 'pos_name'
            arg_flag = func.__code__.co_flags
            if arg_flag % 8 > 4: # varargs
                args[pos_args_no]['type'] = 'var_args'
            if arg_flag % 16 > 8: # varkeywords
                args[-1]['type'] = 'var_keywords'
            defaults = func.__defaults__
            if defaults:
                for arg, default in zip(args[pos_args_no-len(defaults):pos_args_no], defaults):
                    arg['default'] = default
            f.write(f'    def {func_name}(self')
            for arg in args:
                f.write(', ')
                if arg['type'] == 'var_args':
                    f.write('*')
                elif arg['type'] == 'var_keywords':
                    f.write('**')
                f.write(arg['name'])
                if 'default' in arg:
                    f.write(f'={repr(arg["default"])}')
            f.write('):\n')
            doc = func.__doc__
            if doc is not None:
                f.write(f'        """{doc}"""\n')
            f.write('        pass\n\n')

if __name__ == "__main__":
    from test_interface import ConsoleInterface
    analyse_class(ConsoleInterface)