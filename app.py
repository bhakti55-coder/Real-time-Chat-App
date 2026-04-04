from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Secret key is required for secure login sessions
app.config['SECRET_KEY'] = 'my-super-secret-key'
# This creates a file called chat.db in your folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db' 

db = SQLAlchemy(app)
socketio = SocketIO(app)

# --- DATABASE MODEL ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the database file when the app starts
with app.app_context():
    db.create_all()

# --- WEB ROUTES (LOGIN/REGISTER) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return "Username already exists. <a href='/'>Go back</a>"
    
    # Save new user with an encrypted password
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    
    # Log them in automatically
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Find user and verify password
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = username
        return redirect(url_for('index'))
    return "Invalid credentials. <a href='/'>Go back</a>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# --- WEBSOCKET ROUTE ---
@socketio.on('message')
def handle_message(msg):
    # Get the username from the secure session, or call them Anonymous
    username = session.get('username', 'Anonymous')
    
    # Broadcast the username AND the message to everyone
    emit('message', {'user': username, 'text': msg}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
