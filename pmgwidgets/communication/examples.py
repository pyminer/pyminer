if __name__=='__main__':
    from pmgwidgets import BaseClient

    import numpy as np

    x = np.random.random(10) + np.linspace(1, 10, 10)
    y = np.random.random(10) + np.linspace(1, 10, 10)
    print(x)
    c = BaseClient()

    print('set_var')
    c.set_var('x', x)
    c.set_var('y', y)
    c.set_var('z', y)
    c.set_var('w', y)
    c.set_var('t', y)
    c.set_var('y', y)
    c.get_var('x')
    print(c.get_all_vars())
    print(c.get_all_var_names())
    # while (1):
    #     time.sleep(1)