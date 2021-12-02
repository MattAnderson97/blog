from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4,max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4,max=20)])
    email = StringField('email', validators=[InputRequired(), Email(), Length(min=4,max=50)])
    password = PasswordField('password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'), Length(min=8,max=80)])
    confirm = PasswordField('confirm password', validators=[InputRequired(), Length(min=8,max=80)])