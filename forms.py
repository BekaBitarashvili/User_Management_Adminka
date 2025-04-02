from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter Your first name"})
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Enter Your last name"})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Enter Your Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), EqualTo('confirm_password')], render_kw={"placeholder": "Enter Your Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log In")