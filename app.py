from datetime import timedelta
from threading import Lock

from flask import Flask, jsonify, render_template, copy_current_request_context, request
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect, rooms

from config import db, BLACKLIST_TOKEN
from resource.token import TokenRefresh
from resource.users import UserLogin, UserLogout, UserRegister

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "jhjhjhl3bhb3jjbjjhjhjhjhjjhgsfeifeifiefieifeifeifieifeifei"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=6000)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=6000)

api = Api(app)
jwt = JWTManager(app)
socketio = SocketIO(app)

thread = None
thread_lock = Lock()


#############################################################

@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def token_in_blacklist_callback(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST_TOKEN


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error: str):
    return jsonify({
        'description': 'Invalid JWT. Header:Authorization:Bearer {token}'
    }), 422


@jwt.unauthorized_loader
def unauthorized_callback(error: str):
    return jsonify({
        'description': 'JWT not found. Header:Authorization:Bearer {token}'
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': 'Fresh token required.'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked. 😈',
        'error': 'token_revoked'
    }), 401


@jwt.user_claims_loader
def user_claims_callback(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/token_refresh')


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


######################Run#######################################

db.init_app(app)
# socketio.init_app(app)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
