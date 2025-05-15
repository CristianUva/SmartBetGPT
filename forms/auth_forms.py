# forms/auth_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask import current_app

class RegisterForm(FlaskForm):
    """Form for registering a new user"""
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password')])
    terms = BooleanField('Accetto i Termini e Condizioni', validators=[DataRequired(message='Devi accettare i Termini e Condizioni per registrarti')])
    age = BooleanField('Dichiaro di avere 18 o più anni', validators=[DataRequired(message='Devi confermare di avere almeno 18 anni per registrarti')])
    submit = SubmitField('Registrati')
    
    def validate_email(self, email):
        """Check that the email is not already registered"""
        from models.user import User  # Import here to avoid circular imports
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email già registrata. Utilizzare un\'altra email o effettuare il login.')

class LoginForm(FlaskForm):
    """Form for logging in an existing user"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    """Form for requesting a password reset"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Invia link di reset')
    
    def validate_email(self, email):
        """Check that the email exists in the system"""
        from models.user import User  # Import here to avoid circular imports
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email non trovata. Registrati prima di richiedere un reset della password.')

class ResetPasswordForm(FlaskForm):
    """Form for resetting the password after receiving a valid token"""
    password = PasswordField('Nuova Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reimposta Password')
