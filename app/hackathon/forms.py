from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class HackathonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateTimeField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    theme = StringField('Theme', validators=[Optional(), Length(max=100)])
    max_participants = IntegerField('Max Participants', validators=[
        DataRequired(),
        NumberRange(min=1, max=1000)
    ])
    registration_deadline = DateTimeField('Registration Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    is_online = BooleanField('Online Event')
    rules = TextAreaField('Rules & Guidelines', validators=[Optional()])
    prizes = TextAreaField('Prizes', validators=[Optional()])
    tracks = StringField('Tracks (comma-separated)', validators=[Optional()])
    waitlist_enabled = BooleanField('Enable Waitlist')
    submit = SubmitField('Submit')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('normal', 'Normal'),
        ('high', 'High')
    ])
    submit = SubmitField('Post Announcement') 