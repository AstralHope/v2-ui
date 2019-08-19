import atexit
import time
from concurrent.futures import ThreadPoolExecutor

import schedule

__running = True
__thread_pool = ThreadPoolExecutor(1)
__future = None


@atexit.register
def before_exit():
    global __running, __future
    __running = False
    __future = None
    schedule.clear()
    __thread_pool.shutdown(False)


def schedule_job(target, seconds=1):
    schedule.every(seconds).seconds.do(target)


def start_schedule():
    global __future
    if __future:
        return

    def target():
        while __running:
            time.sleep(1)
            try:
                schedule.run_pending()
            except Exception:
                pass

    __future = __thread_pool.submit(target)
