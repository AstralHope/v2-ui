from flask import session


def is_login():
    return 'LOGIN_USER' in session


def login_success(user):
    session['LOGIN_USER'] = user.to_json()


def logout():
    session.pop('LOGIN_USER', True)
