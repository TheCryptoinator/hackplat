from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class TeamForm(FlaskForm):
    name = StringField('Team Name', validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(max=500)
    ])
    max_members = IntegerField('Maximum Team Size', validators=[
        DataRequired(),
        NumberRange(min=2, max=10)
    ])
    submit = SubmitField('Submit') 