import time

t_start_script = time.time()
print(__name__)

import matplotlib.pyplot as plt
import numpy as np

a = np.random.randn(1000 * 100* 100)
print('start_time and prepare data:', time.time() - t_start_script)
print(a.shape)
print(sys.argv)
#   >>>
#print('11123',a)
if __name__ == '__main__':
    t0 = time.time()
    # plt.plot([1, 2, 3, 4, 5, 1])
    plt.hist(a, bins=20,color='red')
    plt.xlabel('haha')
    plt.ylabel('y is lalala')
    print(time.time() - t0)
    print('full time', time.time() - t_start_script)
    plt.show()
