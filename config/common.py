from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
BLACKLIST_TOKEN = set()
db = SQLAlchemy()