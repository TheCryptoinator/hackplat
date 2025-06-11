from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Project
from hackathon_app import db

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects')
def index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)

@projects_bp.route('/projects/<int:id>')
def show(id):
    project = Project.query.get_or_404(id)
    return render_template('projects/show.html', project=project) 