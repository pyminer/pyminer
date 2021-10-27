import subprocess
from pathlib import Path
from typing import Union

import chardet


def system(*args: Union[str, Path]):
    args = [str(arg) for arg in args]
    result = subprocess.run(args=args, capture_output=True)
    stdout = result.stdout
    if stdout:
        print('Out: ')
        stdout = stdout.decode(chardet.detect(result.stdout)['encoding'])
        print(stdout)
    stderr = result.stderr
    if stderr:
        print('Error: ')
        stderr = stderr.decode(chardet.detect(result.stderr)['encoding'])
        print(stderr)
