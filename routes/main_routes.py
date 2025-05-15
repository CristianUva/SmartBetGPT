# routes/main_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from forms.contact_forms import ContactForm
from services.email_service import send_email

# Create blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Send message to admin
            send_email(
                subject=form.subject.data,
                recipient=request.application.config['MAIL_DEFAULT_SENDER'],
                template='contact_message',
                name=form.name.data,
                email=form.email.data,
                message=form.message.data
            )
            
            # Send confirmation to user
            send_email(
                subject="Messaggio ricevuto",
                recipient=form.email.data,
                template='confirmation_email',
                name=form.name.data
            )
            
            flash('Messaggio inviato con successo!', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            flash(f'Errore nell\'invio del messaggio: {str(e)}', 'danger')
    
    return render_template('contact.html', form=form)

@main.route('/legal')
def legal():
    """Legal information page"""
    return render_template('legal.html')

@main.route('/faq')
def faq():
    """Frequently asked questions page"""
    return render_template('faq.html')
