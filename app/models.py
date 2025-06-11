from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='participant')
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    skills = db.Column(db.String(200))
    experience_level = db.Column(db.String(20))
    portfolio_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    created_hackathons = db.relationship('Hackathon', backref='creator', lazy='dynamic')
    team_memberships = db.relationship('TeamMember', backref='user', lazy='dynamic')
    announcements = db.relationship('Announcement', backref='author', lazy='dynamic')
    judge_assignments = db.relationship('Judge', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Hackathon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.String(100))
    theme = db.Column(db.String(100))
    max_participants = db.Column(db.Integer)
    registration_deadline = db.Column(db.DateTime)
    is_online = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='upcoming')
    rules = db.Column(db.Text)
    prizes = db.Column(db.Text)
    tracks = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    waitlist_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teams = db.relationship('Team', backref='hackathon', lazy='dynamic')
    announcements = db.relationship('Announcement', backref='hackathon', lazy='dynamic')
    sponsors = db.relationship('Sponsor', secondary='hackathon_sponsors', backref='hackathons')
    judges = db.relationship('Judge', backref='hackathon', lazy='dynamic')

    def __repr__(self):
        return f'<Hackathon {self.title}>'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    hackathon_id = db.Column(db.Integer, db.ForeignKey('hackathon.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    max_members = db.Column(db.Integer, default=4)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy='dynamic')
    projects = db.relationship('Project', backref='team', lazy='dynamic')

    def __repr__(self):
        return f'<Team {self.name}>'

class TeamMember(db.Model):
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.String(20), default='member')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

    def __repr__(self):
        return f'<TeamMember {self.user_id} in Team {self.team_id}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    github_url = db.Column(db.String(200))
    demo_url = db.Column(db.String(200))
    presentation_url = db.Column(db.String(200))
    status = db.Column(db.String(20), default='in_progress')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    submissions = db.relationship('Submission', backref='project', lazy='dynamic')
    evaluations = db.relationship('Evaluation', backref='project', lazy='dynamic')

    def __repr__(self):
        return f'<Project {self.title}>'

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    submission_type = db.Column(db.String(50))
    file_url = db.Column(db.String(200))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    def __repr__(self):
        return f'<Submission {self.id} for Project {self.project_id}>'

class Judge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hackathon_id = db.Column(db.Integer, db.ForeignKey('hackathon.id'))
    expertise = db.Column(db.String(200))
    assigned_tracks = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    evaluations = db.relationship('Evaluation', backref='judge', lazy='dynamic')

    def __repr__(self):
        return f'<Judge {self.user_id} for Hackathon {self.hackathon_id}>'

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    score = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    criteria_scores = db.Column(db.String(200))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Evaluation {self.id} by Judge {self.judge_id}>'

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hackathon_id = db.Column(db.Integer, db.ForeignKey('hackathon.id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(20), default='normal')

    def __repr__(self):
        return f'<Announcement {self.title}>'

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(200))
    website_url = db.Column(db.String(200))
    contact_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Sponsor {self.name}>'

# Association table for hackathon-sponsor relationship
hackathon_sponsors = db.Table('hackathon_sponsors',
    db.Column('hackathon_id', db.Integer, db.ForeignKey('hackathon.id'), primary_key=True),
    db.Column('sponsor_id', db.Integer, db.ForeignKey('sponsor.id'), primary_key=True),
    db.Column('sponsorship_level', db.String(50)),
    db.Column('contribution', db.String(200)),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 