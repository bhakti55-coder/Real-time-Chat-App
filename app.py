import os # Added for deployment
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# For deployment, we use an environment variable for the secret key if available
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my-super-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'

db = SQLAlchemy(app)
# Use 'eventlet' for high-performance real-time deployment
socketio = SocketIO(app, cors_allowed_origins="*") 

user_current_room = {}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    room = db.Column(db.String(150), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user: return "Exists! <a href='/'>Back</a>"
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = username
        return redirect(url_for('index'))
    return "Invalid! <a href='/'>Back</a>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@socketio.on('join')
def on_join(data):
    username = session.get('username', 'Anonymous')
    new_room = data['room']
    old_room = user_current_room.get(username)
    if old_room and old_room != new_room:
        leave_room(old_room)
        emit('status', {'msg': f'{username} has left to another room.'}, room=old_room)
        old_room_users = [u for u, r in user_current_room.items() if r == old_room and u != username]
        emit('update_users', old_room_users, room=old_room)
    join_room(new_room)
    user_current_room[username] = new_room
    current_room_users = [u for u, r in user_current_room.items() if r == new_room]
    emit('status', {'msg': f'{username} has entered {new_room}.'}, room=new_room)
    emit('update_users', current_room_users, room=new_room)
    past_messages = Message.query.filter_by(room=new_room).order_by(Message.timestamp).all()
    history = [{'user': msg.username, 'text': msg.text, 'time': msg.timestamp.strftime('%I:%M %p') if msg.timestamp else ""} for msg in past_messages]
    emit('load_history', history, to=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in user_current_room:
        room = user_current_room[username]
        del user_current_room[username]
        current_room_users = [u for u, r in user_current_room.items() if r == room]
        emit('update_users', current_room_users, room=room)

@socketio.on('typing')
def handle_typing(data):
    username = session.get('username', 'Anonymous')
    room = data['room']
    emit('user_typing', {'user': username}, room=room, include_self=False)

@socketio.on('stop_typing')
def handle_stop_typing(data):
    room = data['room']
    emit('user_stop_typing', {}, room=room, include_self=False)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    room = data['room']
    text = data['msg']
    new_msg = Message(username=username, room=room, text=text)
    db.session.add(new_msg)
    db.session.commit()
    formatted_time = new_msg.timestamp.strftime('%I:%M %p')
    emit('message', {'user': username, 'text': text, 'time': formatted_time}, room=room)

if __name__ == '__main__':
    # PORT handling for cloud deployment
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)