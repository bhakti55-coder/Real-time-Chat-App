from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db' 

db = SQLAlchemy(app)
socketio = SocketIO(app)

# PRO UPGRADE: Track which room each user is in
# Format: {'Alice': 'General', 'Bob': 'Internship-Group'}
user_current_room = {}

from datetime import datetime  # <--- PASTE 1 GOES HERE
from flask import Flask, render_template, request, session, redirect, url_for
# ... other imports ...

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    room = db.Column(db.String(150), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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

# --- ROOM-SPECIFIC TRACKING LOGIC ---

@socketio.on('join')
def on_join(data):
    username = session.get('username', 'Anonymous')
    new_room = data['room']

    # 1. If they were in an old room, remove them from it
    old_room = user_current_room.get(username)
    if old_room and old_room != new_room:
        leave_room(old_room)
        emit('status', {'msg': f'{username} has left to another room.'}, room=old_room)
        # Update old room's user list
        old_room_users = [u for u, r in user_current_room.items() if r == old_room and u != username]
        emit('update_users', old_room_users, room=old_room)

    # 2. Join the new room
    join_room(new_room)
    user_current_room[username] = new_room

    # 3. Update the new room's user list
    current_room_users = [u for u, r in user_current_room.items() if r == new_room]
    emit('status', {'msg': f'{username} has entered {new_room}.'}, room=new_room)
    emit('update_users', current_room_users, room=new_room)

@socketio.on('join')
def on_join(data):
    username = session.get('username', 'Anonymous')
    new_room = data['room']

    # ... (Keep all your existing room-joining logic here) ...

    # Look for this line (it is usually the last line in your current function):
    # Define who is currently in the room
    current_room_users = [u for u, r in user_current_room.items() if r == new_room]
    emit('update_users', current_room_users, room=new_room)

    # >>> PASTE STEP 3 CODE DIRECTLY BELOW THAT LINE <<<
    
    # 1. Fetch historical messages for this room from the database
    past_messages = Message.query.filter_by(room=new_room).order_by(Message.timestamp).all()
    
    # 2. Format them into a list
    history = [{'user': msg.username, 'text': msg.text} for msg in past_messages]
    
    # 3. Send history ONLY to the user who just joined
    emit('load_history', history, to=request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in user_current_room:
        room = user_current_room[username]
        del user_current_room[username] # Remove them from tracking
        # Tell the room they left
        current_room_users = [u for u, r in user_current_room.items() if r == room]
        emit('update_users', current_room_users, room=room)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    room = data['room']
    text = data['msg']
    
    # A. CREATE THE RECORD: Create a new row for our "notebook"
    new_msg = Message(username=username, room=room, text=text)
    
    # B. SAVE IT: Tell the database to add this row and save it permanently
    db.session.add(new_msg)
    db.session.commit()
    
    # C. SHOUT IT: Now tell everyone in the room what was said
    emit('message', {'user': username, 'text': text}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
