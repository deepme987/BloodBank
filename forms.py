from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, DecimalField
from wtforms.validators import DataRequired, Email
from pymongo import MongoClient, errors


class RegisterForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Phone', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
