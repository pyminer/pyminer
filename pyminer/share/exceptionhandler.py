from functools import wraps
import traceback

def exception_handler(f):
    '''
    异常处理装饰器。
    使用后可以捕获异常，避免异常退出。
    异常退出时返回值为None。为了代码安全性，一般只适合装饰返回值为None的类型。
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            traceback.print_exc()
            return
    return decorated

if __name__=='__main__':
    @exception_handler
    def func(aaaa,bbbb):
        return ("aaa"+'aaa',)

    print(func(0,1))