from threading import Lock

from flask import render_template, copy_current_request_context, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect, rooms

from config.common import app

socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading",
                    message_queue=app.config['CELERY_RESULT_BACKEND'])

def config_app_socket():
    return socketio



