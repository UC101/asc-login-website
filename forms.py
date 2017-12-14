from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired

class SignupForm(FlaskForm):
    email = StringField('email',
        validators=[DataRequired(),Email()])

    password = PasswordField('password',
        validators=[DataRequired()])

    submit = SubmitField('Sign Up')


class ShortAnswerForm(FlaskForm):
    label = 'NOTHING'
    answer = StringField('answer',
        validators=[DataRequired()])

    submit = SubmitField('submit')

    def __init__(self,question):
        label = question
