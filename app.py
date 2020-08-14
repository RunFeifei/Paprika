from config.api import config_app_api
from config.celery import config_app_celery
from config.common import db, app
from config.jwt import config_app_jwt
from config.redis import clear_app_cache
from config.socket import config_app_socket, socketio
from main.events import onEvents

config_app_celery()
config_app_api()
config_app_jwt()
config_app_socket()
onEvents()

db.init_app(app)
# socketio.init_app(app)

# host必须是本地IP
if __name__ == '__main__':
    db.init_app(app)
    socketio.run(app, debug=True, port=5000, host='10.180.5.207')


@app.teardown_appcontext
def on_shut_down(exception):
    clear_app_cache()


@app.before_first_request
def on_app_first_request():
    clear_app_cache()
