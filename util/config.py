import os

from base.models import Setting
from init import db, BASE_DIR


def __read_v2_template_config():
    with open(os.path.join(BASE_DIR, 'template_config.json'), encoding='utf-8') as f:
        return f.read()


def get_setting_value(setting):
    if setting.value_type.startswith('text'):
        return setting.value
    elif setting.value_type == 'int':
        return int(setting.value)
    elif setting.value_type == 'bool':
        return setting.value.lower() == 'true'


def __get(key, default=None):
    setting = Setting.query.filter_by(key=key).first()
    if setting:
        return get_setting_value(setting)
    else:
        return default


def contains_id(setting_id):
    return Setting.query.filter_by(id=setting_id).count() > 0


def update_setting(setting_id, key, name, value, value_type='text'):
    if setting_id and contains_id(setting_id):
        Setting.query.filter_by(id=setting_id).update({'name': name, 'value': value, 'value_type': value_type})
    else:
        setting = Setting(key, name, value, value_type)
        db.session.add(setting)
    db.session.commit()


def all_settings():
    return Setting.query.all()


def get_port():
    return __get('port', 65432)


def get_cert_file():
    return __get('cert_file', '')


def get_key_file():
    return __get('key_file', '')


def get_login_title():
    return __get('login_title', '登录')


def get_v2_config_path():
    return __get('v2_config_path', '/etc/v2ray/config.json')


def get_v2_restart_cmd():
    return __get('v2_restart_cmd', 'systemctl restart v2ray')


def get_v2_stop_cmd():
    return __get('v2_stop_cmd', 'systemctl stop v2ray')


def get_v2_start_cmd():
    return __get('v2_start_cmd', 'systemctl start v2ray')


def get_v2_config_check_interval():
    return __get('v2_config_check_interval', 60)


def get_v2_template_config():
    return __get('v2_template_config')


def get_traffic_job_interval():
    return __get('traffic_job_interval', 60)


def get_base_path():
    return __get('base_path', '')


def get_current_version():
    return '4.0.0'


def add_if_not_exist(setting, update=False):
    if Setting.query.filter_by(key=setting.key).count() > 0:
        if update:
            Setting.query.filter_by(key=setting.key).update({
                'name': setting.name,
                'value': setting.value,
                'value_type': setting.value_type,
            })
        return
    db.session.add(setting)


def reset_config():
    init_db(True)


def init_db(update=False):
    add_if_not_exist(Setting(
        'port', '面板网页端口', '65432', 'int',
        '', True), update)
    add_if_not_exist(Setting(
        'base_path', '面板网页根路径', '', 'text',
        '谨慎修改！！！可以填写你的个性网页根路径，例如 /v2-ui，默认为空。若填写则必须以 / 开头，不能以 / 结尾，填错会导致无法访问面板', True), update)
    add_if_not_exist(Setting(
        'cert_file', '面板ssl证书路径', '', 'text',
        '谨慎修改！！！需填写一个绝对路径，修改错误会导致无法启动面板', True), update)
    add_if_not_exist(Setting(
        'key_file', '面板ssl密钥路径', '', 'text',
        '谨慎修改！！！需填写一个绝对路径，修改错误会导致无法启动面板', True), update)
    add_if_not_exist(Setting(
        'login_title', '登录页标题', '登录', 'text',
        '', False), update)
    add_if_not_exist(Setting(
        'v2_config_path', 'v2ray配置文件路径', '/etc/v2ray/config.json', 'text',
        '谨慎修改！！！生成的v2ray配置会写入此项配置的文件中，一般无需修改', False), update)
    add_if_not_exist(Setting(
        'v2_template_config', 'v2ray配置文件模板', __read_v2_template_config(), 'textarea',
        '谨慎修改！！！请确保你对v2ray的配置非常熟悉，请不要删除关于api的配置', False), update)
    add_if_not_exist(Setting(
        'v2_config_check_interval', '账号生效时间（秒）', '60', 'int',
        '数值过小会导致CPU使用率上升，填0或负数后果自负', True), update)
    add_if_not_exist(Setting(
        'v2_restart_cmd', '重启v2ray命令', 'systemctl restart v2ray', 'text',
        '当v2ray需重启时，面板会自动运行此命令来重启v2ray，一般无需修改', False), update)
    add_if_not_exist(Setting(
        'traffic_job_interval', '统计流量间隔时间（秒）', '60', 'int',
        '数值过小会导致CPU使用率上升，填0或负数后果自负', True), update)
    db.session.commit()


init_db()
