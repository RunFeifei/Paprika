from flask import render_template, copy_current_request_context
from flask_socketio import emit, join_room, rooms, leave_room, close_room, disconnect

from config.celery import async_emit_msg
from config.common import app, MESSAGE_TYPE
from config.socket import socketio
from model.message import Message


def onEvents():
    pass


######################SocketIO#######################################

@app.route('/')
def sessions():
    return render_template('session.html')


@socketio.on('connect')
def on_connect():
    pass


@socketio.on('join_room')
def on_join_rooms(message):
    uid_from = message['uid_from']
    room_from = message['room_from']
    join_room(room_from)
    joined_rooms = rooms()
    app.logger.error('{}--join_room--{}--joined_rooms_is---{}'.format(uid_from, room_from, joined_rooms))
    text = message['text']
    msg_type = message['type']
    is_send_to_server = message['is_send_to_server']
    time_client = message['time_client']
    room_to = message['room_to']
    message = Message(text, msg_type, is_send_to_server, time_client, room_from, room_to, uid_from, uid_from)
    message.save()
    message_id = message.id
    app.logger.error('message_id-{}--{}--saved to db'.format(message_id, message.text))
    if room_from in joined_rooms:
        data = {
            'id': message_id,
            'text': 'join_room_ok',
            'room_from': room_from,
            'type': MESSAGE_TYPE.MESSAGE_ACK.value,
            'uid_from': uid_from,
        }
        async_emit_msg.delay('join_room', data, room=room_from)


@socketio.on('message')
def on_message(message):
    pass


@socketio.on('my_event')
def test_message(message):
    app.logger.info('#########my_event    {}#########'.format(message))
    async_emit_msg('my_response', {'data': message['data'], 'count': 'receive_count'}).delay()


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
