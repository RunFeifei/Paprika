from config.common import db


class Message(db.Model):
    __tablename__ = 'messages_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False)

    def __init__(self, name, msg_type):
        self.name = name
        self.type = msg_type

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
