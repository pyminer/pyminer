# import pretty_errors
import time
print('start_time',time.time())
t0=time.time()
import sys
import tornado.platform.asyncio as async_io
from pyminer2.pmappmodern import main


if sys.platform == 'win32':
    async_io.asyncio.set_event_loop_policy(
        async_io.asyncio.WindowsSelectorEventLoopPolicy())
t2 = time.time()
print('time spent for importing modules',t2-t0)
main()
