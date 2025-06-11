import os
from dotenv import load_dotenv
from datetime import timedelta
import redis

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
    
    # Redis settings
    REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'test123')
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Session settings
    SESSION_TYPE = 'redis'
    SESSION_REDIS = REDIS_URL
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Cache settings
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
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
    # Development-specific Redis settings
    REDIS_DB = 1  # Use a different DB for development
    CACHE_DEFAULT_TIMEOUT = 60  # Shorter cache timeout for development

class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = 0
    SESSION_COOKIE_SECURE = True
    
    # Production-specific settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    # Production-specific Redis settings
    REDIS_DB = 0  # Use default DB for production
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
    REDIS_URL = os.environ.get('TEST_REDIS_URL', 'redis://:test123@redis:6379/1')
    WTF_CSRF_ENABLED = False
    # Testing-specific Redis settings
    REDIS_DB = 2  # Use a different DB for testing
    CACHE_DEFAULT_TIMEOUT = 0  # Disable caching for tests

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 