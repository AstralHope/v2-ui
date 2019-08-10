import json

from sqlalchemy import Column, Integer, String, BIGINT, Boolean

from init import db


class Inbound(db.Model):
    __tablename__ = 'inbound'
    id = Column(Integer, primary_key=True, autoincrement=True)
    port = Column(Integer, unique=True, nullable=False)
    listen = Column(String(50), default='0.0.0.0')
    protocol = Column(String(50), nullable=False)
    settings = Column(String, nullable=False)
    stream_settings = Column(String, nullable=False)
    tag = Column(String(255), default='', unique=True, nullable=False)
    sniffing = Column(String, default='{"enabled":true,"destOverride":["http","tls"]}')
    remark = Column(String(255), default='', nullable=False)
    up = Column(BIGINT, default=0, nullable=False)
    down = Column(BIGINT, default=0, nullable=False)
    enable = Column(Boolean, default=True, nullable=False)

    def __init__(self, port=None, listen=None, protocol=None,
                 settings=None, stream_settings=None, sniffing=None, remark=None):
        self.port = port
        self.listen = listen
        self.protocol = protocol
        self.settings = settings
        self.stream_settings = stream_settings
        self.tag = 'inbound-%d' % self.port
        self.sniffing = sniffing
        self.remark = remark
        self.up = 0
        self.down = 0
        self.enable = True

    def to_json(self):
        return {
            'id': self.id,
            'port': self.port,
            'listen': self.listen,
            'protocol': self.protocol,
            'settings': json.loads(self.settings, encoding='utf-8'),
            'stream_settings': json.loads(self.stream_settings, encoding='utf-8'),
            'sniffing': json.loads(self.sniffing, encoding='utf-8'),
            'remark': self.remark,
            'up': self.up,
            'down': self.down,
            'enable': self.enable,
        }

    def to_v2_json(self):
        return {
            'port': self.port,
            'listen': self.listen,
            'protocol': self.protocol,
            'settings': json.loads(self.settings, encoding='utf-8'),
            'streamSettings': json.loads(self.stream_settings, encoding='utf-8'),
            'sniffing': json.loads(self.sniffing, encoding='utf-8'),
            'tag': self.tag,
        }

    def to_v2_str(self):
        return json.dumps(self.to_v2_json(), indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
