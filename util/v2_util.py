import codecs
import json
import logging
import re
import sys
from enum import Enum
from threading import Timer

from util import config, list_util, cmd_util, server_info, file_util
from v2ray.exceptions import V2rayException
from v2ray.models import Inbound


class Protocols(Enum):
    VMESS = 'vmess'
    SHADOWSOCKS = 'shadowsocks'
    DOKODEMO = 'dokodemo-door'
    SOCKS = 'socks'
    HTTP = 'http'


def gen_v2_config_from_db():
    inbounds = Inbound.query.filter_by(enable=True).all()
    inbounds = [inbound.to_v2_json() for inbound in inbounds]
    v2_config = json.loads(config.get_v2_template_config())
    v2_config['inbounds'] += inbounds
    return v2_config


def read_v2_config():
    try:
        path = config.get_v2_config_path()
        file_util.touch(path)
        with open(path, encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error('An error occurred while reading the v2ray configuration file: ' + str(e))
        return None


def write_v2_config(v2_config):
    v2_config = json.dumps(v2_config, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': '))
    if read_v2_config() == v2_config:
        return
    try:
        with open(config.get_v2_config_path(), 'w', encoding='utf-8') as f:
            f.write(v2_config)
        restart(True)
    except Exception as e:
        logging.error('An error occurred while writing the v2ray configuration file: ' + str(e))


def __get_api_address_port():
    template_config = json.loads(config.get_v2_template_config(), encoding='utf-8')
    inbounds = template_config['inbounds']
    api_inbound = list_util.get(inbounds, 'tag', 'api')
    return api_inbound['listen'], api_inbound['port']


def __get_stat_code():
    return server_info.get_status()['v2']['code']


def is_running():
    return __get_stat_code() == 0


def restart(now=False):
    def f():
        cmd_util.exec_cmd(config.get_v2_restart_cmd())
    if now:
        f()
    else:
        Timer(3, f).start()


def start():
    if is_running():
        raise V2rayException('v2ray already running')

    def f():
        cmd_util.exec_cmd(config.get_v2_start_cmd())
    Timer(3, f).start()


def stop():
    if not is_running():
        raise V2rayException('v2ray has stopped')

    def f():
        cmd_util.exec_cmd(config.get_v2_stop_cmd())
    Timer(3, f).start()


try:
    __api_address, __api_port = __get_api_address_port()
    if not __api_address or __api_address == '0.0.0.0':
        __api_address = '127.0.0.1'
except Exception as e:
    logging.error('Failed to open v2ray api, please reset all panel settings.')
    logging.error(str(e))
    sys.exit(-1)
__traffic_pattern = re.compile('stat:\s*<\s*name:\s*"inbound>>>'
                               '(?P<tag>[^>]+)>>>traffic>>>(?P<type>uplink|downlink)"(\s*value:\s*(?P<value>\d+))?')


__v2ctl_cmd = config.get_v2ctl_cmd_path()


def __get_v2ray_api_cmd(address, service, method, pattern, reset):
    cmd = '%s api --server=%s:%d %s.%s \'pattern: "%s" reset: %s\''\
          % (__v2ctl_cmd, address, __api_port, service, method, pattern, reset)
    return cmd


def get_inbounds_traffic(reset=True):
    if __api_port < 0:
        logging.warning('v2ray api port is not configured')
        return None
    cmd = __get_v2ray_api_cmd('', 'StatsService', 'QueryStats', '', 'true' if reset else 'false')
    result, code = cmd_util.exec_cmd(cmd)
    if code != 0:
        logging.warning('v2ray api code %d' % code)
        return None
    inbounds = []
    for match in __traffic_pattern.finditer(result):
        tag = match.group('tag')
        tag = codecs.getdecoder('unicode_escape')(tag)[0]
        tag = tag.encode('ISO8859-1').decode('utf-8')
        if tag == 'api':
            continue
        _type = match.group('type')
        value = match.group('value')
        if not value:
            value = 0
        else:
            value = int(value)
        inbound = list_util.get(inbounds, 'tag', tag)
        if inbound:
            inbound[_type] = value
        else:
            inbounds.append({
                'tag': tag,
                _type: value
            })
    return inbounds
