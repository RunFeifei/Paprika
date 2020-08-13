from flask import render_template, copy_current_request_context, request
from flask_socketio import emit, join_room, rooms, leave_room, disconnect

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

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


# Flask有报错
@socketio.on('on_disconnect')
def on_disconnect_request(message):
    text = message['text']
    type = message['type']
    uid_from = message['uid_from']
    uid_to = message['uid_to']
    room_from = message['room_from']
    room_to = message['room_to']

    @copy_current_request_context
    def do_disconnect():
        app.logger.error('{}--do_disconnect--copy_current_request_context'.format(uid_from))
        disconnect()

    data = {
        'id': uid_from,
        'text': 'do_disconnect',
        'room_from': room_from,
        'room_to': room_to,
        'uid_from': uid_from,
        'uid_to': uid_to,
        'type': MESSAGE_TYPE.MESSAGE_BROADCAST.value,
    }
    app.logger.error('on_disconnect-{}'.format(message))
    result = async_emit_msg.delay('do_disconnect', data, broadcast=True)

    def on_message_result(body):
        print(body)
        status = body['status']
        if status == 'SUCCESS':
            do_disconnect()

    result.get(on_message=on_message_result, propagate=False)


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
        async_emit_msg.delay('join_room', data, broadcast=True)


@socketio.on('message')
def on_message(message):
    uid_from = message['uid_from']
    room_from = message['room_from']
    text = message['text']
    msg_type = message['type']
    is_send_to_server = message['is_send_to_server']
    time_client = message['time_client']
    room_to = message['room_to']
    message = Message(text, msg_type, is_send_to_server, time_client, room_from, room_to, uid_from, uid_from)
    message.save()
    message_id = message.id
    app.logger.error('message_id-{}--{}--saved to db'.format(message_id, message.text))


@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': 'receive_count'})


@socketio.on('my_room_event')
def send_room_message(message):
    emit('my_response',
         {'data': message['data'], 'count': 'receive_count'},
         room=message['room'])
