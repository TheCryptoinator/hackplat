import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    FLASK_APP = os.environ.get('FLASK_APP', 'hackathon_app.py')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_DEBUG = int(os.environ.get('FLASK_DEBUG', 1))
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://hackathon:test123@db:5432/hackathon')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_session'
    SESSION_FILE_THRESHOLD = 500
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'hackathon:'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Cache settings
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = '/tmp/flask_cache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '200 per day'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = ['your-email@example.com']
    
    # Pagination
    POSTS_PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True
    CACHE_DEFAULT_TIMEOUT = 60  # Shorter cache timeout for development

class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = 0
    SESSION_COOKIE_SECURE = True
    
    # Production-specific settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    CACHE_DEFAULT_TIMEOUT = 3600  # Longer cache timeout for production
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
    }

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    FLASK_DEBUG = 1
    SESSION_COOKIE_SECURE = False
    
    # Test-specific settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'postgresql://hackathon:test123@db:5432/hackathon_test')
    WTF_CSRF_ENABLED = False
    CACHE_DEFAULT_TIMEOUT = 0  # Disable caching for tests

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 