from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db' 

db = SQLAlchemy(app)
socketio = SocketIO(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

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

# --- WEEK 3: ROOM LOGIC ---
@socketio.on('join')
def on_join(data):
    username = session.get('username', 'Anonymous')
    room = data['room']
    join_room(room)
    emit('status', {'msg': username + ' has entered the room: ' + room}, room=room)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    room = data['room']
    # Broadcast specifically to the ROOM
    emit('message', {'user': username, 'text': data['msg']}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
