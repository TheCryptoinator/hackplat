from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from datetime import datetime, timedelta
import os
import psycopg2
from psycopg2.extras import DictCursor
from functools import wraps

app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object('config.ProductionConfig')
elif env == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect(app)

# Configure session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_FILE_THRESHOLD'] = 500
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'hackathon:'

# Initialize Cache with filesystem backend
cache = Cache(app)

# Initialize Rate Limiter with memory backend
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["200 per day", "50 per hour"]
)

# Initialize Session
Session(app)

# Import models
from models import User, Hackathon, Team, Project, TeamMember, TeamInvitation, TeamJoinRequest, TeamUpdate, ProjectUpdate, ProjectFeedback, ProjectScreenshot, ProjectResource, HackathonResource, HackathonSponsor, HackathonPrize, HackathonSchedule, HackathonRule, HackathonCategory, HackathonTag, HackathonSkill, HackathonTechnology, HackathonFeature, HackathonRequirement, HackathonSubmission, HackathonSubmissionFeedback, HackathonSubmissionScore, HackathonSubmissionComment, HackathonSubmissionVote, HackathonSubmissionReport, HackathonSubmissionAward, HackathonSubmissionPrize, HackathonSubmissionCertificate, HackathonSubmissionBadge, HackathonSubmissionMedal, HackathonSubmissionTrophy, HackathonSubmissionCup, HackathonSubmissionRibbon, HackathonSubmissionSticker, HackathonSubmissionPatch, HackathonSubmissionPin, HackathonSubmissionButton, HackathonSubmissionTShirt, HackathonSubmissionHoodie, HackathonSubmissionHat, HackathonSubmissionBag, HackathonSubmissionMug, HackathonSubmissionBottle, HackathonSubmissionSticker, HackathonSubmissionPatch, HackathonSubmissionPin, HackathonSubmissionButton, HackathonSubmissionTShirt, HackathonSubmissionHoodie, HackathonSubmissionHat, HackathonSubmissionBag, HackathonSubmissionMug, HackathonSubmissionBottle

# Import blueprints
from auth import auth_bp
from hackathons import hackathons_bp
from teams import teams_bp
from projects import projects_bp
from admin import admin_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(hackathons_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(admin_bp)

# Create database tables
with app.app_context():
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Main routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

# Database connection
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            app.config['SQLALCHEMY_DATABASE_URI'],
            cursor_factory=DictCursor
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize database
def init_db():
    with app.app_context():
        conn = get_db()
        c = conn.cursor()
        
        # Drop existing tables if they exist
        c.execute('DROP TABLE IF EXISTS hackathon_sponsors CASCADE')
        c.execute('DROP TABLE IF EXISTS sponsors CASCADE')
        c.execute('DROP TABLE IF EXISTS messages CASCADE')
        c.execute('DROP TABLE IF EXISTS announcements CASCADE')
        c.execute('DROP TABLE IF EXISTS evaluations CASCADE')
        c.execute('DROP TABLE IF EXISTS judges CASCADE')
        c.execute('DROP TABLE IF EXISTS submissions CASCADE')
        c.execute('DROP TABLE IF EXISTS projects CASCADE')
        c.execute('DROP TABLE IF EXISTS team_members CASCADE')
        c.execute('DROP TABLE IF EXISTS teams CASCADE')
        c.execute('DROP TABLE IF EXISTS hackathons CASCADE')
        c.execute('DROP TABLE IF EXISTS users CASCADE')
        
        # Create tables
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                full_name VARCHAR(100),
                bio TEXT,
                skills TEXT,
                experience_level VARCHAR(20),
                portfolio_url VARCHAR(255),
                github_url VARCHAR(255),
                linkedin_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Add other table creation statements here...
        
        conn.commit()
        conn.close()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 