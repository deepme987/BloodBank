from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, RadioField, DecimalField
from wtforms.validators import DataRequired, Email
from wtforms import SelectField
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

class BloodDonateForm(FlaskForm):
    bg = SelectField('BloodGroup', choices = [('ap', 'A(+ve)'), ('an', 'A(-ve)'), ('bp', 'B(+ve)'), ('bn', 'B(-ve)'), ('abp', 'AB(+ve)'), ('abn', 'AB(-ve)'), ('op', 'O(+ve)'), ('on', 'O(-ve)')], validators=[DataRequired()])
    NoOfUnits = SelectField('NoOfUnits', choices = [('2', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gendre = RadioField('Gendre', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],  validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])

class SearchBloodForm(FlaskForm):
    bg = SelectField('BloodGroup', choices=[('ap', 'A(+ve)'), ('an', 'A(-ve)'), ('bp', 'B(+ve)'), ('bn', 'B(-ve)'), ('abp', 'AB(+ve)'), ('abn', 'AB(-ve)'), ('op', 'O(+ve)'), ('on', 'O(-ve)')], validators=[DataRequired()])

class BloodRequestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gendre = RadioField('Gendre', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],  validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
