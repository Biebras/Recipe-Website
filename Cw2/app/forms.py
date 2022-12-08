from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

# create forms
class RegisterForm(FlaskForm):
    # set validations for every variable
    Username = StringField("Username", validators=[DataRequired(), Length(4, 16)])
    Password = PasswordField("New Password", validators=[DataRequired(), EqualTo('ConfirmPassword', message='Passwords must match'), Length(4, 16)])
    ConfirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), Length(4, 16)])
    ProfileUrl = StringField("Profile Url", validators=[Length(0, 300)])
    Terms = BooleanField("Agree?", validators=[DataRequired()])

class LoginForm(FlaskForm):
    Username = StringField("Username", validators=[DataRequired(), Length(4, 16)])
    Password = PasswordField("New Password", validators=[DataRequired(), Length(4, 16)])