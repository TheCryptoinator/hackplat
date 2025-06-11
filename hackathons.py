from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Hackathon
from hackathon_app import db

hackathons_bp = Blueprint('hackathons', __name__)

@hackathons_bp.route('/hackathons')
def index():
    hackathons = Hackathon.query.all()
    return render_template('hackathons/index.html', hackathons=hackathons)

@hackathons_bp.route('/hackathons/<int:id>')
def show(id):
    hackathon = Hackathon.query.get_or_404(id)
    return render_template('hackathons/show.html', hackathon=hackathon) 