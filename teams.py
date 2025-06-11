from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Team, TeamMember
from hackathon_app import db

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams')
def index():
    teams = Team.query.all()
    return render_template('teams/index.html', teams=teams)

@teams_bp.route('/teams/<int:id>')
def show(id):
    team = Team.query.get_or_404(id)
    return render_template('teams/show.html', team=team) 