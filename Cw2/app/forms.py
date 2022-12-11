from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FieldList, FormField, Form
from wtforms.validators import DataRequired, Length, EqualTo

# create forms
class RegisterForm(FlaskForm):
    # set validations for every variable
    username = StringField("Username", validators=[DataRequired(), Length(4, 16)])
    password = PasswordField("New Password", validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match'), Length(4, 16)])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), Length(4, 16)])
    profileUrl = StringField("Profile Url", validators=[Length(0, 300)])
    terms = BooleanField("Agree?", validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(4, 16)])
    password = PasswordField("New Password", validators=[DataRequired(), Length(4, 16)])
    rememberMe = BooleanField("Remember?")

class IngrediantForm(Form):
    ingrediant = StringField("Ingrediant", validators=[DataRequired(), Length(1, 100)])
    quantity = StringField("Ingrediant", validators=[DataRequired(), Length(1, 7)])

class RecipeForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(1, 100)])
    ingrediants = FieldList(FormField(IngrediantForm), min_entries=1, max_entries=20)
    instructions = TextAreaField("Instructions", validators=[DataRequired(), Length(1, 2000)])
    image_url = StringField("Image Url", validators=[DataRequired(), Length(0, 300)])