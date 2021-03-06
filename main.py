from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from app.firestore_service import get_messages, put_message, put_sub_message, update_message, update_sub_message, delete_message, like_message, like_sub_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,  cors_allowed_origins='*')


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
    emit('get_messages', res, broadcast=True)


@socketio.on('get_messages')
def handle_get_messages():
    messages = get_messages()
    emit('get_messages', messages)


@socketio.on('sub_message')
def handle_put_sub_message(message):
    res = put_sub_message(message['message_id'],
                          message['message'], message['userEmail'])
    emit('get_messages', res, broadcast=True)


@socketio.on('update_message')
def handle_update_message(message):
    res = update_message(message['message_id'], message['message'])
    emit('get_messages', res, broadcast=True)


@socketio.on('update_sub_message')
def handle_update_sub_message(data):
    res = update_sub_message(
        data['message_id'], data['sub_message_id'], data['message'])
    emit('get_messages', res, broadcast=True)


@socketio.on('delete_message')
def handle_delete_message(data):
    res = delete_message(data.get('message_id'), data.get('sub_message_id'))
    emit('get_messages', res, broadcast=True)


@socketio.on('like_message')
def handle_like_message(data):
    res = like_message(data['message_id'], data['is_like'])
    emit('get_messages', res, broadcast=True)


@socketio.on('like_sub_message')
def handle_like_sub_message(data):
    res = like_sub_message(data['message_id'],
                     data['sub_message_id'], data['is_like'])
    emit('get_messages', res, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
