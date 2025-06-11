from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import User, Hackathon, Team
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
    hackathons = Hackathon.query.filter(
        Hackathon.end_date >= datetime.utcnow()
    ).order_by(Hackathon.start_date.asc()).all()
    return render_template('index.html', title='Home', hackathons=hackathons)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        hackathons = Hackathon.query.order_by(Hackathon.start_date.desc()).all()
    else:
        hackathons = Hackathon.query.filter(
            Hackathon.end_date >= datetime.utcnow()
        ).order_by(Hackathon.start_date.asc()).all()
    
    teams = Team.query.join(Hackathon).add_columns(
        Hackathon.title.label('hackathon_title')
    ).all()
    
    return render_template('dashboard.html', 
                         title='Dashboard',
                         hackathons=hackathons,
                         teams=teams,
                         role=current_user.role)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')

@bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='Settings') 