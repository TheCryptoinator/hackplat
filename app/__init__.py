from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from flask_talisman import Talisman
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import structlog
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
cache = Cache()
session = Session()
limiter = Limiter(key_func=get_remote_address)
compress = Compress()
talisman = Talisman()
cors = CORS()
metrics = PrometheusMetrics()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    session.init_app(app)
    limiter.init_app(app)
    compress.init_app(app)
    talisman.init_app(app)
    cors.init_app(app)
    metrics.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Configure logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer()
        ]
    )
    
    # Initialize Sentry in production
    if not app.debug and not app.testing:
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=config_name
        )
    
    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.hackathon import bp as hackathon_bp
    app.register_blueprint(hackathon_bp, url_prefix='/hackathon')
    
    from app.team import bp as team_bp
    app.register_blueprint(team_bp, url_prefix='/team')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Register error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    # Register CLI commands
    from app.cli import register_commands
    register_commands(app)
    
    return app

from app import models 