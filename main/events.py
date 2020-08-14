import time

from flask import render_template, request
from flask_socketio import emit, join_room, rooms, leave_room

from config.celery import async_emit_msg
from config.common import app, MESSAGE_TYPE
from config.redis import update_sid_uid_map, add_online_uids, get_uid_with_sid, remove_online_uids
from config.socket import socketio
from model.message import Message
from model.users import UserModel


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
def on_disconnect():
    sid = request.sid
    uid = get_uid_with_sid(sid)
    remove_online_uids(uid)
    user = UserModel.find_by_id(uid)
    print('Client disconnected--{}--{}--{}'.format(sid, uid, user.to_json()))
    message = Message('disconnect_broadcast', MESSAGE_TYPE.MESSAGE_BROADCAST.value, False,
                      int(round(time.time() * 1000)), user.room_private, user.room_private, uid, uid)
    async_emit_msg.delay('disconnect_broadcast', message.to_json(), broadcast=True)


@socketio.on('connect_broadcast')
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
        update_sid_uid_map(sid=request.sid, uid=uid_from)
        add_online_uids(uid_from)
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
