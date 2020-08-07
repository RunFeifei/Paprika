import time

from config.common import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    is_send_to_server = db.Column(db.Boolean, nullable=False)
    time_client = db.Column(db.Integer, nullable=False)
    time_server = db.Column(db.Integer, nullable=False)
    # room_from 如果是私聊 那么就是自己的room_private;群聊就是群聊本身的room
    # room_to 如果是私聊 那么就是对方的room_private;群聊就是群聊本身的room
    room_from = db.Column(db.String(100), nullable=False)
    room_to = db.Column(db.String(100), nullable=False)
    # uid是用户id 这个是固定不变的
    # request.sid 这个是变化的 所以这个是不需要落库的
    # 既然request.sid是变化的 那么每个client自动加入的room也是变化的
    # 所以要实现私聊 需要每个client加入一个固定的以uid编码生成的room id
    # 如果是私聊都非空,如果是群聊uid_to为空
    uid_to = db.Column(db.String(100), nullable=True)
    uid_from = db.Column(db.String(100), nullable=False)

    def __init__(self, text, msg_type, is_send_to_server, time_client, room_from, room_to, uid_from, uid_to):
        self.text = text
        self.type = msg_type
        self.is_send_to_server = is_send_to_server
        self.time_client = time_client
        self.time_server = int(round(time.time() * 1000))
        self.room_from = room_from
        self.room_to = room_to
        self.uid_from = uid_from
        self.uid_to = uid_to

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
