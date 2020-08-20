import logging
import platform
import subprocess
from threading import Timer
from typing import Tuple

__is_windows = platform.system() == 'Windows'


def exec_cmd(cmd, timeout=10) -> Tuple[str, int]:
    code = -100
    p = None
    try:
        def close_task():
            if p:
                p.terminate()
        task = Timer(timeout, close_task)
        task.start()
        encoding = 'gbk' if __is_windows else 'utf-8'
        with subprocess.Popen(['sh', '-c', cmd], shell=False, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding=encoding) as process:
            p = process
            code = process.wait(timeout)
            result = process.stdout.read()
            p = None
            task.cancel()
        return result, code
    except Exception as e:
        if not __is_windows:
            logging.warning(f'execute \"{cmd}\" failed: {e}')
        return '', code
    finally:
        if p:
            p.terminate()
