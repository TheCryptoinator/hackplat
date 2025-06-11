from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Hackathon, Team, Project
from hackathon_app import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def index():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    
    users = User.query.all()
    hackathons = Hackathon.query.all()
    teams = Team.query.all()
    projects = Project.query.all()
    
    return render_template('admin/index.html',
                         users=users,
                         hackathons=hackathons,
                         teams=teams,
                         projects=projects) 