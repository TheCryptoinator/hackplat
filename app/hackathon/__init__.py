from flask import Blueprint

bp = Blueprint('hackathon', __name__)

from app.hackathon import routes 