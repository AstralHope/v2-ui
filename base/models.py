from sqlalchemy import Column, Integer, String, Boolean

from init import db


class Msg(dict):
    def __init__(self, success=False, msg='', obj=None):
        super(Msg, self).__init__({'success': success, 'msg': msg, 'obj': obj})


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'username': self.username,
            'password': self.password,
        }


class Setting(db.Model):
    __tablename__ = 'setting'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, unique=True, nullable=False, default='')
    name = Column(String, unique=True, nullable=False, default='')
    value = Column(String, nullable=False, default='')
    value_type = Column(String, nullable=False, default='text')
    tip = Column(String, nullable=False, default='')
    need_restart = Column(Boolean, nullable=False, default=True)

    def __init__(self, key, name, value, value_type, tip='', need_restart=False):
        self.key = key
        self.name = name
        self.value = value
        self.value_type = value_type
        self.tip = tip
        self.need_restart = need_restart

    def to_json(self):
        return {
            'id': self.id,
            'key': self.key,
            'name': self.name,
            'value': self.value,
            'value_type': self.value_type,
            'tip': self.tip,
            'need_restart': self.need_restart,
        }
