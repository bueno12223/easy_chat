from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from app.firestore_service import get_messages, put_message, put_sub_message, update_message, update_sub_message, delete_message, delete_sub_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['GET'])
def messages():
    messages = get_messages()
    return messages


@socketio.on('message')
def handle_put_message(data):
    res = put_message(data['message'], data['userEmail'])
    send(res, broadcast=True)


@socketio.on('get_messages')
def handle_get_messages():
    messages = get_messages()
    send(messages, broadcast=True)


@socketio.on('sub_message')
def handle_put_sub_message(message):
    res = put_sub_message(message['message_id'],
                          message['message'], message['userEmail'])
    emit('sub_message', res)


@socketio.on('update_message')
def handle_update_message(message):
    update_message(message['message_id'], message['message'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
