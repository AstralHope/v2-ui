import atexit

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def before_exit():
    if scheduler.running:
        scheduler.shutdown(wait=False)


atexit.register(before_exit)
