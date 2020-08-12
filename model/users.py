import time

from config.common import db
from tools.tools import MD5


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    room_private = db.Column(db.String(50), nullable=False)
    time_register = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.room_private = MD5(username)
        self.time_register = int(round(time.time() * 1000))

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_paginate(cls, page=0, per_page=10):
        return UserModel.query.order_by(UserModel.time_register.desc()).paginate(page=page, per_page=per_page,
                                                                                 error_out=False, max_per_page=20)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict
