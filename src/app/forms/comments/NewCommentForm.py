from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import InputRequired, Length


class NewCommentForm(FlaskForm):
    content = StringField('Share your thoughts', validators=[InputRequired(), Length(max=250, message="Comments can only be up to %(max)d characters long")])
    parent = HiddenField('Parent')
    post = HiddenField('Post', validators=[InputRequired()])