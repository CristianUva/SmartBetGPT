# services/email_service.py
from flask import render_template
from flask_mail import Message
from flask import current_app

def send_email(subject, recipient, template, **kwargs):
    """
    Send an email using Flask-Mail
    
    Args:
        subject: Email subject
        recipient: Recipient email address
        template: Template name (without extension)
        **kwargs: Variables to pass to the template
    
    Returns:
        True if sent successfully, False otherwise
    """
    try:
        mail = current_app.extensions['mail']
        msg = Message(subject, recipients=[recipient])
        msg.body = render_template(f'{template}.txt', **kwargs)
        msg.html = render_template(f'{template}.html', **kwargs)
        
        # Print debug info
        print(f"Invio email a {recipient} con oggetto '{subject}'")
        
        mail.send(msg)
        print(f"Email inviata con successo a {recipient}")
        return True
    except Exception as e:
        error_message = f"Errore nell'invio dell'email a {recipient}: {str(e)}"
        current_app.logger.error(error_message)
        print(error_message)
        return False
