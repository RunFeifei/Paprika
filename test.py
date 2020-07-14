from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testkey123'
socketio = SocketIO(app)



@app.route('/')  # we definately need this
def sessions():
    return render_template('session.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)  # we definately need this
    # 0.0.0.0 means listening to any device that submits to that port
