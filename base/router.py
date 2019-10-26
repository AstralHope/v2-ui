from flask import Blueprint, Response, render_template, request, jsonify, redirect, url_for
from flask_babel import gettext

from base.models import Msg, User
from init import db
from util import config, session_util

base_bp = Blueprint('base', __name__)


@base_bp.route('/')
def index():
    if session_util.is_login():
        return redirect(url_for('v2ray.index'))
    from init import common_context
    return render_template('index.html',
                           login_title=config.get_login_title(),
                           **common_context)


@base_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user is not None:
        session_util.login_success(user)
        return jsonify(Msg(True, gettext('login success')))
    return jsonify(Msg(False, gettext('username or password wrong')))


@base_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session_util.logout()
    return redirect(url_for('base.index'))


@base_bp.route('/robots.txt')
def robots():
    return Response('User-agent: *\n' + 'Disallow: /', 200, headers={
        'Content-Type': 'text/plain'
    })


def init_user():
    if User.query.count() == 0:
        db.session.add(User('admin', 'admin'))
        db.session.commit()


init_user()
