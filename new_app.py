import pretty_errors
from pyminer_new.pmappmodern import main
import tornado.platform.asyncio as async_io
import sys
if sys.platform=='win32':
    async_io.asyncio.set_event_loop_policy(async_io.asyncio.WindowsSelectorEventLoopPolicy())
main()