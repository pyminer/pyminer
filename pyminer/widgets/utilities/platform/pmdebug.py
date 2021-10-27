import sys
import pickle

sys.path.append(r'/')


def test1():
    print(123)


def test():
    test1()
    print(123456)


def insight(name, var):
    from lib.comm import set_var

    if name not in ['globals', 'os'] and (not name.startswith('__')):
        try:
            print('set_var')
            pickle.dumps(var)
            set_var(name, var, 'debugger')
            print('set_var')
        except:
            d = {}
            import traceback
            traceback.print_exc()
            for k in dir(var):
                try:
                    attr = getattr(var, k)
                    pickle.dumps(attr)
                    d[k] = attr
                except:
                    d[k] = str(getattr(var, k))
            print(name, '=', d)
            set_var(name, d, 'debugger')
