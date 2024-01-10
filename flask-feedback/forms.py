from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_bycrpt import Bycrypt


class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")

class LoginForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField("Feeback Title", validators=[InputRequired()])
    content = StringField("Feedback Content", validators=[InputRequired()])
    
