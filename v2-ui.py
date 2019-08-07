import logging
import os
import sys

import tornado.log
import tornado.options
from tornado import web, wsgi
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from init import app, BASE_DIR
from util import config


def logging_init():
    logging.basicConfig(filename='/etc/v2-ui/v2-ui.log',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
                        level=logging.WARN)
    tornado.log.access_log.setLevel('ERROR')
    tornado.log.app_log.setLevel('ERROR')
    tornado.log.gen_log.setLevel('ERROR')


def get_ssl_option():
    cert_file = config.get_cert_file()
    key_file = config.get_key_file()
    if cert_file != '' and key_file != '':
        return {
            'certfile': cert_file,
            'keyfile': key_file,
        }
    return None


def main():
    base_path = config.get_base_path()
    settings = {
        'static_path': os.path.join(BASE_DIR, 'static'),
        'static_url_prefix': base_path + '/static/',
    }
    wsgi_app = wsgi.WSGIContainer(app)
    handlers = []
    if base_path:
        handlers += [(base_path, web.RedirectHandler, dict(url=base_path + '/'))]
    handlers += [(base_path + r'/.*', web.FallbackHandler, dict(fallback=wsgi_app))]
    tornado_app = web.Application(handlers, **settings)
    http_server = HTTPServer(tornado_app, ssl_options=get_ssl_option())
    http_server.listen(config.get_port())
    print("面板监听端口为 %d" % config.get_port())
    IOLoop.current().start()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'resetconfig':
            config.reset_config()
            print('所有面板设置已重置为默认值，现在请重启面板')
        elif sys.argv[1] == 'resetuser':
            from base.models import User
            from init import db
            User.query.update({'username': 'admin', 'password': 'admin'})
            db.session.commit()
            print('用户名和密码已重置为admin，现在请重启面板')
        else:
            print('无效指令')
            print('resetconfig：重置所有面板设置为默认值')
            print('resetuser：重置用户名与密码为admin')
    else:
        logging_init()
        try:
            main()
        except BaseException as e:
            logging.error(str(e))
            raise e
