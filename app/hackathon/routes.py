from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.hackathon import bp
from app.hackathon.forms import HackathonForm, AnnouncementForm
from app.models import Hackathon, Team, TeamMember, Announcement, Sponsor
from datetime import datetime

@bp.route('/<int:id>')
@login_required
def details(id):
    hackathon = Hackathon.query.get_or_404(id)
    
    # Get teams with member counts
    teams = Team.query.filter_by(hackathon_id=id).all()
    for team in teams:
        team.member_count = TeamMember.query.filter_by(team_id=team.id).count()
    
    # Get user's team if any
    user_team = Team.query.join(TeamMember).filter(
        Team.hackathon_id == id,
        TeamMember.user_id == current_user.id
    ).first()
    
    # Get announcements
    announcements = Announcement.query.filter_by(hackathon_id=id).order_by(
        Announcement.created_at.desc()
    ).all()
    
    # Get sponsors
    sponsors = Sponsor.query.join(
        'hackathons'
    ).filter_by(id=id).all()
    
    # Check if user is registered
    is_registered = TeamMember.query.join(Team).filter(
        Team.hackathon_id == id,
        TeamMember.user_id == current_user.id
    ).first() is not None
    
    return render_template('hackathon/details.html',
                         hackathon=hackathon,
                         teams=teams,
                         user_team=user_team,
                         announcements=announcements,
                         sponsors=sponsors,
                         is_registered=is_registered)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role not in ['admin', 'organizer']:
        flash('You do not have permission to create hackathons')
        return redirect(url_for('main.dashboard'))
    
    form = HackathonForm()
    if form.validate_on_submit():
        hackathon = Hackathon(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            creator_id=current_user.id,
            location=form.location.data,
            theme=form.theme.data,
            max_participants=form.max_participants.data,
            registration_deadline=form.registration_deadline.data,
            is_online=form.is_online.data,
            rules=form.rules.data,
            prizes=form.prizes.data,
            tracks=form.tracks.data,
            capacity=form.max_participants.data,
            waitlist_enabled=form.waitlist_enabled.data
        )
        db.session.add(hackathon)
        db.session.commit()
        flash('Hackathon created successfully!')
        return redirect(url_for('hackathon.details', id=hackathon.id))
    
    return render_template('hackathon/create.html', title='Create Hackathon', form=form)

@bp.route('/<int:id>/register', methods=['POST'])
@login_required
def register(id):
    hackathon = Hackathon.query.get_or_404(id)
    
    # Check if registration is still open
    if datetime.utcnow() > hackathon.registration_deadline:
        flash('Registration is closed')
        return redirect(url_for('hackathon.details', id=id))
    
    # Check if user is already registered
    if TeamMember.query.join(Team).filter(
        Team.hackathon_id == id,
        TeamMember.user_id == current_user.id
    ).first():
        flash('You are already registered for this hackathon')
        return redirect(url_for('hackathon.details', id=id))
    
    # Check capacity
    current_participants = TeamMember.query.join(Team).filter(
        Team.hackathon_id == id
    ).count()
    
    if current_participants >= hackathon.max_participants:
        if not hackathon.waitlist_enabled:
            flash('Sorry, this hackathon has reached its capacity')
            return redirect(url_for('hackathon.details', id=id))
        else:
            flash('You have been added to the waitlist')
    
    # Create a new team for the user
    team = Team(
        name=f"Team {current_user.username}",
        description="Personal team",
        hackathon_id=id,
        creator_id=current_user.id
    )
    db.session.add(team)
    db.session.flush()  # Get the team ID
    
    # Add user to the team
    team_member = TeamMember(
        team_id=team.id,
        user_id=current_user.id,
        role='leader'
    )
    db.session.add(team_member)
    db.session.commit()
    
    flash('Successfully registered for the hackathon!')
    return redirect(url_for('hackathon.details', id=id))

@bp.route('/<int:id>/announcement', methods=['POST'])
@login_required
def create_announcement(id):
    if current_user.role not in ['admin', 'organizer']:
        flash('You do not have permission to create announcements')
        return redirect(url_for('hackathon.details', id=id))
    
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            hackathon_id=id,
            title=form.title.data,
            content=form.content.data,
            created_by=current_user.id,
            priority=form.priority.data
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully!')
    
    return redirect(url_for('hackathon.details', id=id))

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    if current_user.role not in ['admin', 'organizer']:
        flash('You do not have permission to edit hackathons')
        return redirect(url_for('hackathon.details', id=id))
    
    hackathon = Hackathon.query.get_or_404(id)
    form = HackathonForm(obj=hackathon)
    
    if form.validate_on_submit():
        form.populate_obj(hackathon)
        db.session.commit()
        flash('Hackathon updated successfully!')
        return redirect(url_for('hackathon.details', id=id))
    
    return render_template('hackathon/edit.html', title='Edit Hackathon', form=form)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if current_user.role not in ['admin', 'organizer']:
        flash('You do not have permission to delete hackathons')
        return redirect(url_for('hackathon.details', id=id))
    
    hackathon = Hackathon.query.get_or_404(id)
    db.session.delete(hackathon)
    db.session.commit()
    flash('Hackathon deleted successfully!')
    return redirect(url_for('main.dashboard')) 