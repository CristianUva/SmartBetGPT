# forms/contact_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    """Form for contact messages"""
    name = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Oggetto', validators=[DataRequired()])
    message = StringField('Messaggio', validators=[DataRequired()])
    submit = SubmitField('Invia')
