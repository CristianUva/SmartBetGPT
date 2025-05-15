# routes/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms.auth_forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from services.email_service import send_email
from datetime import datetime

# Create blueprint
auth = Blueprint('auth', __name__)

# Define database instance
db = None

def init_routes(app_db):
    """Initialize database instance from app.py"""
    global db
    db = app_db

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        from models.user import User  # Import here to avoid circular import
        hashed_password = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Generate confirmation token
            token = user.get_confirmation_token()
            confirmation_url = url_for('auth.confirm_email', token=token, _external=True)
            
            # Send confirmation email
            email_sent = send_email(
                subject='SmartBetGPT - Conferma la tua email',
                recipient=user.email,
                template='email_confirmation',
                name=user.name,
                confirmation_url=confirmation_url
            )
            
            if email_sent:
                flash('Registrazione avvenuta con successo! Ti abbiamo inviato una email di conferma.', 'success')
            else:
                flash('Registrazione avvenuta con successo, ma c\'è stato un problema nell\'invio dell\'email di conferma.', 'warning')
            
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Si è verificato un errore durante la registrazione: {str(e)}', 'danger')
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login an existing user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        from models.user import User  # Import here to avoid circular import
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login effettuato con successo!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Login fallito. Controlla email e password.', 'danger')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Logout the current user"""
    logout_user()
    flash('Sei stato disconnesso.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/confirm-email/<token>')
def confirm_email(token):
    """Confirm a user's email address"""
    from models.user import User  # Import here to avoid circular import
    
    user = User.verify_confirmation_token(token)
    if user is None:
        flash('Il link di conferma non è valido o è scaduto.', 'danger')
        return redirect(url_for('main.index'))
    
    user.email_confirmed = True
    user.email_confirmed_on = datetime.utcnow()
    db.session.commit()
    
    flash('La tua email è stata confermata! Ora puoi accedere.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgotten password requests"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        from models.user import User  # Import here to avoid circular import
        user = User.query.filter_by(email=form.email.data).first()
        
        # Generate reset token
        token = user.get_reset_token()
        reset_url = url_for('auth.reset_password', token=token, email=user.email, _external=True)
        
        # Send reset email
        email_sent = send_email(
            subject='SmartBetGPT - Reimposta la tua password',
            recipient=user.email,
            template='password_reset_email',
            name=user.name,
            reset_url=reset_url
        )
        
        if email_sent:
            flash('Ti abbiamo inviato un\'email con le istruzioni per reimpostare la password.', 'info')
        else:
            flash('Si è verificato un problema nell\'invio dell\'email. Riprova più tardi.', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset a user's password"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Check if email parameter is provided
    email = request.args.get('email', '')
    if not email:
        flash('Link di reset non valido.', 'danger')
        return redirect(url_for('auth.login'))
    
    from models.user import User  # Import here to avoid circular import
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Il link di reset non è valido o è scaduto.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        user.clear_reset_token()
        db.session.commit()
        flash('La tua password è stata aggiornata! Ora puoi accedere.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form)
