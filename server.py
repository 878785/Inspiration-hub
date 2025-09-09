from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for testing

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inspiration.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey2025"  # Update with a secure key in production

# Create SQLAlchemy instance
db = SQLAlchemy(app)  # Initialize directly with app

# Define models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    coins = db.Column(db.Integer, default=0)
    ideas_submitted = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ideas = db.relationship('Idea', backref='user', lazy=True)
    chats = db.relationship('Chat', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)

class Idea(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    votes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    logger.info("Database tables created or verified at %s", datetime.now().isoformat())

# ---------- ROUTES FOR TEMPLATES ---------- #
@app.route('/')
def index():
    return render_template('index.html')  # Default route now serves index.html

@app.route('/mindmap')
def mindmap():
    return render_template('mindmap.html')

@app.route('/kanban')
def kanban():
    return render_template('kanban.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/study')
def study():
    return render_template('study.html')

@app.route('/job')
def job():
    return render_template('job.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/idea')
def idea():
    return render_template('idea.html')

@app.route('/code')
def code():
    return render_template('code.html')

@app.route('/mock')
def mock():
    return render_template('mock.html')

@app.route('/time')
def time():
    return render_template('time.html')

@app.route('/flashcard')
def flashcard():
    return render_template('flashcard.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/swot')
def swot():
    return render_template('swot.html')

@app.route('/goal')
def goal():
    return render_template('goal.html')

@app.route('/wireframe')
def wireframe():
    return render_template('wireframe.html')

@app.route('/color')
def color():
    return render_template('color.html')

@app.route('/pitch')
def pitch():
    return render_template('pitch.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/task')
def task():
    return render_template('task.html')

@app.route('/resource')
def resource():
    return render_template('resource.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/mindfulness')
def mindfulness():
    return render_template('mindfulness.html')

@app.route('/freelance')
def freelance():
    return render_template('freelance.html')

@app.route('/whiteboard')
def whiteboard():
    return render_template('whiteboard.html')

@app.route('/summarizer')
def summarizer():
    return render_template('summarizer.html')

@app.route('/jobapp')
def jobapp():
    return render_template('jobapp.html')

@app.route('/eventfeedback')
def eventfeedback():
    return render_template('eventfeedback.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

# ---------- API ENDPOINTS ---------- #
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            logger.warning("Signup attempt with missing fields at %s", datetime.now().isoformat())
            return jsonify({"error": "Username, email, and password required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            logger.warning("Signup attempt with existing username: %s at %s", username, datetime.now().isoformat())
            return jsonify({"error": "Username already exists"}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        logger.info("New user signed up: %s at %s", username, datetime.now().isoformat())

        session['user'] = username
        return jsonify({"message": "Signup successful!", "username": username, "email": email}), 201
    except Exception as e:
        logger.error("Signup error: %s at %s", str(e), datetime.now().isoformat())
        return jsonify({"error": "Server error during signup"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        logger.debug("Attempting login for user: %s, user found: %s", username, user is not None)
        if user and check_password_hash(user.password, password):
            session['user'] = username
            logger.info("User logged in: %s at %s", username, datetime.now().isoformat())
            return jsonify({"message": "Login successful!", "username": username, "email": user.email})
        logger.warning("Failed login attempt for username: %s at %s", username, datetime.now().isoformat())
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        logger.error("Login error: %s at %s", str(e), datetime.now().isoformat())
        return jsonify({"error": "Server error during login"}), 500

@app.route('/api/logout')
def logout():
    session.pop("user", None)
    logger.info("User logged out at %s", datetime.now().isoformat())
    return jsonify({"message": "Logged out successfully"})

@app.route('/api/check-login')
def check_login():
    return jsonify({"logged_in": "user" in session, "username": session.get("user")})

@app.route('/api/profile', methods=['GET'])
def profile():
    if "user" not in session:
        return jsonify({"error": "Please log in"}), 401
    user = User.query.filter_by(username=session["user"]).first()
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email,
            "coins": user.coins,
            "ideas_submitted": user.ideas_submitted,
            "created_at": user.created_at.isoformat()
        })
    return jsonify({"error": "User not found"}), 404

@app.route('/api/ideas', methods=['GET', 'POST'])
def manage_ideas():
    if request.method == 'POST':
        if "user" not in session:
            return jsonify({"error": "Please log in"}), 401
        data = request.get_json()
        category = data.get('category')
        description = data.get('description')
        if not category or not description or len(description) < 10:
            return jsonify({"error": "Invalid idea data"}), 400
        user = User.query.filter_by(username=session["user"]).first()
        idea = Idea(user_id=user.id, category=category, description=description)
        db.session.add(idea)
        db.session.commit()
        user.ideas_submitted += 1
        user.coins = user.ideas_submitted // 10
        db.session.commit()
        logger.info("Idea submitted by %s at %s", user.username, datetime.now().isoformat())
        return jsonify({"message": "Idea submitted", "id": idea.id}), 201
    elif request.method == 'GET':
        ideas = [{"id": i.id, "username": i.user.username, "category": i.category, "description": i.description, "votes": i.votes, "timestamp": i.timestamp.isoformat()} for i in Idea.query.all()]
        return jsonify(ideas)

@app.route('/api/chats', methods=['GET', 'POST'])
def manage_chats():
    if request.method == 'GET':
        chats = [{"username": u.username, "message": c.message, "timestamp": c.timestamp.isoformat()} for c in Chat.query.all() for u in User.query.filter_by(id=c.user_id)]
        return jsonify(chats)
    elif request.method == 'POST':
        if "user" not in session:
            return jsonify({"error": "Please log in"}), 401
        data = request.get_json()
        message = data.get('message')
        if not message:
            return jsonify({"error": "Message required"}), 400
        user = User.query.filter_by(username=session["user"]).first()
        chat = Chat(user_id=user.id, message=message)
        db.session.add(chat)
        db.session.commit()
        logger.info("Chat sent by %s at %s", user.username, datetime.now().isoformat())
        return jsonify({"message": "Chat sent"}), 200

@app.route('/api/projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'GET':
        projects = [{"id": p.id, "name": p.name, "user_id": p.user_id} for p in Project.query.all()]
        return jsonify(projects)
    elif request.method == 'POST':
        if "user" not in session:
            return jsonify({"error": "Please log in"}), 401
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({"error": "Project name required"}), 400
        user = User.query.filter_by(username=session["user"]).first()
        project = Project(user_id=user.id, name=name)
        db.session.add(project)
        db.session.commit()
        logger.info("Project created by %s at %s", user.username, datetime.now().isoformat())
        return jsonify({"message": "Project created", "id": project.id}), 201

@app.route('/api/activities', methods=['GET'])
def get_activities():
    activities = [f"{u.username} {a.description} at {a.timestamp.isoformat()}" for a in Activity.query.all() for u in User.query.filter_by(id=a.user_id)]
    return jsonify(activities)

@app.route('/api/vote-idea', methods=['POST'])
def vote_idea():
    if "user" not in session:
        return jsonify({"error": "Please log in"}), 401
    data = request.get_json()
    idea_id = data.get('ideaId')
    vote_type = data.get('voteType')
    if not idea_id or vote_type not in ['up']:
        return jsonify({"error": "Invalid vote data"}), 400

    user = User.query.filter_by(username=session["user"]).first()
    existing_vote = db.session.query(Idea).filter(Idea.id == idea_id).first()
    if not existing_vote:
        return jsonify({"error": "Idea not found"}), 404

    idea = existing_vote
    idea.votes += 1
    owner = User.query.get(idea.user_id)
    if owner and owner.id != user.id:
        owner.coins += 1
        db.session.commit()
        logger.info("Coin awarded to %s for vote on idea %s at %s", owner.username, idea_id, datetime.now().isoformat())

    db.session.commit()
    logger.info("Vote recorded by %s on idea %s at %s", session["user"], idea_id, datetime.now().isoformat())
    return jsonify({"message": "Vote recorded", "votes": idea.votes, "owner_coins": owner.coins if owner else 0})

# ---------- MAIN ---------- #
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)