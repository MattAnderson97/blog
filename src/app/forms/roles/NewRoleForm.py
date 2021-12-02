from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired, Length


class NewRoleForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4,max=20)])
    is_admin = BooleanField('Administrator')
    can_write = BooleanField('Author')