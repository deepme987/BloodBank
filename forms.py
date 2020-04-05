
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, RadioField, DecimalField
from wtforms.validators import DataRequired, Email
from wtforms import SelectField
from pymongo import MongoClient, errors
from datetime import datetime


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
                        validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Phone', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class BloodDonateForm(FlaskForm):
    bg = SelectField('Blood Group', choices=[('A+', 'A(+ve)'), ('A-', 'A(-ve)'), ('B+', 'B(+ve)'), ('B-', 'B(-ve)'),
                                             ('AB+', 'AB(+ve)'), ('AB-', 'AB(-ve)'), ('O+', 'O(+ve)'), ('O-', 'O(-ve)')],
                     validators=[DataRequired()])
    NoOfUnits = SelectField('Number Of Units', choices=[('2', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                            validators=[DataRequired()])

    def return_data(self, _id):
        data = self.data
        data["id"] = _id
        data["timestamp"] = str(datetime.now().date())
        del data["csrf_token"]
        return data


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])


class UpdateProfileForm(FlaskForm):
    name = StringField('Name')
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])


class SearchBloodForm(FlaskForm):
    bg = SelectField('Blood Group', choices=[('A+', 'A(+ve)'), ('A-', 'A(-ve)'), ('B+', 'B(+ve)'), ('B-', 'B(-ve)'),
                                             ('AB+', 'AB(+ve)'), ('AB-', 'AB(-ve)'), ('O+', 'O(+ve)'), ('O-', 'O(-ve)')],
                     validators=[DataRequired()])


class BloodRequestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gendre = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
                        validators=[DataRequired()])
    bg = SelectField('Blood Group', choices=[('A+', 'A(+ve)'), ('A-', 'A(-ve)'), ('B+', 'B(+ve)'), ('B-', 'B(-ve)'),
                                             ('AB+', 'AB(+ve)'), ('AB-', 'AB(-ve)'), ('O+', 'O(+ve)'),
                                             ('O-', 'O(-ve)')],
                     validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])

    def return_data(self):
        data = self.data
        data["timestamp"] = str(datetime.now().date())
        del data["csrf_token"]
        return data
