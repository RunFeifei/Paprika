from config.api import config_app_api
from config.celery import config_app_celery
from config.common import db, app
from config.jwt import config_app_jwt
from config.socket import config_app_socket, socketio

config_app_celery()
config_app_api()
config_app_jwt()
config_app_socket()

db.init_app(app)
# socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
