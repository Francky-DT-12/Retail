"""
Utilitaires pour l'envoi d'emails
"""

from flask import current_app, render_template
from flask_mail import Message
from RetailShop import mail  # À décommenter après configuration


def send_email(to, subject, template, **kwargs):
    """
    Envoyer un email avec template
    
    Args:
        to (str): Adresse email destinataire
        subject (str): Sujet de l'email
        template (str): Nom du template (sans .html)
        **kwargs: Variables pour le template
    """
    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            html=render_template(f'emails/{template}.html', **kwargs),
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False


def send_registration_confirmation(user_email, user_name):
    """Envoyer un email de confirmation d'inscription"""
    return send_email(
        to=user_email,
        subject="Bienvenue sur RetailShop !",
        template="registration_confirmation",
        user_name=user_name
    )


def send_order_confirmation(user_email, user_name, order_details):
    """Envoyer un email de confirmation de commande"""
    return send_email(
        to=user_email,
        subject="Confirmation de commande - RetailShop",
        template="order_confirmation",
        user_name=user_name,
        order_details=order_details
    )


def send_admin_notification(order_details):
    """Notifier l'admin d'une nouvelle commande"""
    admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@retailshop.com')
    return send_email(
        to=admin_email,
        subject="Nouvelle commande reçue",
        template="admin_order_notification",
        order_details=order_details
    )
