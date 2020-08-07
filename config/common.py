from enum import unique, Enum

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BLACKLIST_TOKEN = set()
db = SQLAlchemy()


@unique
class MESSAGE_TYPE(Enum):
    MESSAGE_CHAT_GROUP = 0
    MESSAGE_CHAT_PRIVATE = 1
    MESSAGE_JOIN_ROOM = 2
    MESSAGE_EXIT_ROOM = 3
    MESSAGE_ACK = 4
    MESSAGE_BROADCAST = 5


