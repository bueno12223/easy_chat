from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/message', methods=['GET'])
def messages():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send(message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
