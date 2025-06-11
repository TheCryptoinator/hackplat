from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.team import bp
from app.team.forms import TeamForm
from app.models import Team, TeamMember, User, Hackathon

@bp.route('/create/<int:hackathon_id>', methods=['GET', 'POST'])
@login_required
def create(hackathon_id):
    hackathon = db.session.query(Hackathon).get_or_404(hackathon_id)
    
    # Check if user is already in a team for this hackathon
    existing_team = db.session.query(Team).join(TeamMember).filter(
        Team.hackathon_id == hackathon_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if existing_team:
        flash('You are already in a team for this hackathon.', 'warning')
        return redirect(url_for('hackathon.details', hackathon_id=hackathon_id))
    
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(
            name=form.name.data,
            description=form.description.data,
            hackathon_id=hackathon_id,
            max_members=form.max_members.data
        )
        db.session.add(team)
        db.session.flush()  # Get team ID
        
        # Add creator as team leader
        member = TeamMember(
            team_id=team.id,
            user_id=current_user.id,
            role='leader'
        )
        db.session.add(member)
        db.session.commit()
        
        flash('Team created successfully!', 'success')
        return redirect(url_for('hackathon.details', hackathon_id=hackathon_id))
    
    return render_template('team/create.html', form=form, hackathon=hackathon)

@bp.route('/join/<int:team_id>')
@login_required
def join(team_id):
    team = db.session.query(Team).get_or_404(team_id)
    
    # Check if user is already in a team for this hackathon
    existing_team = db.session.query(Team).join(TeamMember).filter(
        Team.hackathon_id == team.hackathon_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if existing_team:
        flash('You are already in a team for this hackathon.', 'warning')
        return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))
    
    # Check if team is full
    if len(team.members) >= team.max_members:
        flash('This team is already full.', 'warning')
        return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))
    
    # Add user to team
    member = TeamMember(
        team_id=team.id,
        user_id=current_user.id,
        role='member'
    )
    db.session.add(member)
    db.session.commit()
    
    flash('Successfully joined the team!', 'success')
    return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))

@bp.route('/leave/<int:team_id>')
@login_required
def leave(team_id):
    team = db.session.query(Team).get_or_404(team_id)
    member = db.session.query(TeamMember).filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first_or_404()
    
    # Check if user is the team leader
    if member.role == 'leader':
        flash('Team leaders cannot leave their team. Please transfer leadership first.', 'warning')
        return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))
    
    db.session.delete(member)
    db.session.commit()
    
    flash('Successfully left the team.', 'success')
    return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))

@bp.route('/transfer-leadership/<int:team_id>/<int:user_id>')
@login_required
def transfer_leadership(team_id, user_id):
    team = db.session.query(Team).get_or_404(team_id)
    current_leader = db.session.query(TeamMember).filter_by(
        team_id=team_id,
        user_id=current_user.id,
        role='leader'
    ).first_or_404()
    
    new_leader = db.session.query(TeamMember).filter_by(
        team_id=team_id,
        user_id=user_id
    ).first_or_404()
    
    current_leader.role = 'member'
    new_leader.role = 'leader'
    db.session.commit()
    
    flash('Team leadership transferred successfully.', 'success')
    return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))

@bp.route('/edit/<int:team_id>', methods=['GET', 'POST'])
@login_required
def edit(team_id):
    team = db.session.query(Team).get_or_404(team_id)
    member = db.session.query(TeamMember).filter_by(
        team_id=team_id,
        user_id=current_user.id,
        role='leader'
    ).first_or_404()
    
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        team.max_members = form.max_members.data
        db.session.commit()
        
        flash('Team updated successfully!', 'success')
        return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))
    
    return render_template('team/edit.html', form=form, team=team)

@bp.route('/remove-member/<int:team_id>/<int:user_id>')
@login_required
def remove_member(team_id, user_id):
    team = db.session.query(Team).get_or_404(team_id)
    leader = db.session.query(TeamMember).filter_by(
        team_id=team_id,
        user_id=current_user.id,
        role='leader'
    ).first_or_404()
    
    member = db.session.query(TeamMember).filter_by(
        team_id=team_id,
        user_id=user_id
    ).first_or_404()
    
    if member.role == 'leader':
        flash('Cannot remove the team leader.', 'warning')
        return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id))
    
    db.session.delete(member)
    db.session.commit()
    
    flash('Member removed from team.', 'success')
    return redirect(url_for('hackathon.details', hackathon_id=team.hackathon_id)) 