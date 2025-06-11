from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import psycopg2
from psycopg2.extras import DictCursor
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
import redis
from functools import wraps

app = Flask(__name__)

# Load configuration
app.config.from_object('config.ProductionConfig')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Redis with fallback to filesystem session
try:
    redis_client = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        password=app.config['REDIS_PASSWORD'],
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5
    )
    # Test connection
    redis_client.ping()
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis_client
except (redis.ConnectionError, redis.TimeoutError):
    print("Redis connection failed, falling back to filesystem session")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
    app.config['SESSION_FILE_THRESHOLD'] = 500
    redis_client = None

# Initialize Cache with fallback
if redis_client:
    cache = Cache(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': app.config['REDIS_URL'],
        'CACHE_DEFAULT_TIMEOUT': 300
    })
else:
    cache = Cache(app, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': '/tmp/flask_cache',
        'CACHE_DEFAULT_TIMEOUT': 300
    })

# Initialize Rate Limiter with fallback
if redis_client:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=app.config['RATELIMIT_STORAGE_URL']
    )
else:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri="memory://"
    )

# Initialize Session
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

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