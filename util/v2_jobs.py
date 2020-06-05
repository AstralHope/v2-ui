import threading
import time
import calendar

from init import db
from util import config, v2_util
from util.schedule_util import schedule_job
from v2ray.models import Inbound

__lock = threading.Lock()
__v2_config_changed = True


def v2_config_change(func):
    def inner(*args, **kwargs):
        global __v2_config_changed
        result = func(*args, **kwargs)
        __v2_config_changed = True
        return result
    inner.__name__ = func.__name__
    return inner


def check_v2_config_job():
    global __v2_config_changed
    if __v2_config_changed:
        with __lock:
            v2_config = v2_util.gen_v2_config_from_db()
            v2_util.write_v2_config(v2_config)
            __v2_config_changed = False


def traffic_job():
    with __lock:
        if not v2_util.is_running():
            return
        traffics = v2_util.get_inbounds_traffic()
        if not traffics:
            return
        for traffic in traffics:
            upload = int(traffic.get('uplink', 0))
            download = int(traffic.get('downlink', 0))
            tag = traffic['tag']
            Inbound.query.filter_by(tag=tag).update({'up': Inbound.up + upload, 'down': Inbound.down + download})
        db.session.commit()


def reset_traffic_job():
    with __lock:
        if not v2_util.is_running():
            return
        year = time.strftime('%Y', time.localtime())
        month = time.strftime('%m', time.localtime())
        day = time.strftime('%d', time.localtime())
        end_day = calendar.monthrange(int(year), int(month))[1]
        days = config.get_reset_traffic_job_days()
        if end_day < days:
            days = end_day
        if int(day) == days:
            Inbound.query.update({'up': 0, 'down': 0})
            db.session.commit()


def init():
    schedule_job(check_v2_config_job, config.get_v2_config_check_interval())
    schedule_job(traffic_job, config.get_traffic_job_interval())
    schedule_job(reset_traffic_job, 24 * 60 * 60)
