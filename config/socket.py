from threading import Lock

from flask import render_template, copy_current_request_context, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect, rooms

from config.common import app

socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading",
                    message_queue=app.config['CELERY_RESULT_BACKEND'])

thread = None
thread_lock = Lock()


def config_app_socket():
    return socketio


######################SocketIO#######################################

@app.route('/')
def sessions():
    return render_template('session.html')


@socketio.on('ping')
def test_message1():
    socketio.emit('client', {'data': 'Connected', 'count': 0})
    app.logger.error('#########test_message1#########')


@socketio.on('my_event')
def test_message(message):
    app.logger.info('#########my_event    {}#########'.format(message))
    emit('my_response',
         {'data': message['data'], 'count': 'receive_count'})


@socketio.on('my_broadcast_event')
def test_broadcast_message(message):
    emit('my_response',
         {'data': message['data'], 'count': 'receive_count'},
         broadcast=True)


@socketio.on('join')
def join(message):
    join_room(message['room'])
    app.logger.info('##### {} entered {}'.format(request.sid, message['room']))
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': 'receive_count'})


@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': 'receive_count'})


@socketio.on('close_room')
def close(message):
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': 'receive_count'},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event')
def send_room_message(message):
    emit('my_response',
         {'data': message['data'], 'count': 'receive_count'},
         room=message['room'])


@socketio.on('disconnect_request')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': 'receive_count'},
         callback=can_disconnect)


@socketio.on('my_ping')
def ping_pong(message):
    emit('my_pong')
    app.logger.info('#####ping_pong____{}'.format(message))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        # socketio.emit('my_response', {'data': 'Server generated event app.py', 'count': count})


@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('testroom')
def test_room():
    app.logger.info('#########testroom#########')
    # 只有room0收到了
    emit('room', request.sid + ' has entered the room.', room='room0')
    # 只有room0收到了
    emit('room', 'emit to all rooms', )
    # 未加入room也收到了
    emit('room', 'broadcast to all rooms', broadcast=True)
