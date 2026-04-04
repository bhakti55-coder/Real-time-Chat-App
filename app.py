from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# This handles the main webpage
@app.route('/')
def index():
    return render_template('index.html')

# This handles receiving a message and sending it to EVERYONE
@socketio.on('message')
def handle_message(msg):
    print('Message received: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)