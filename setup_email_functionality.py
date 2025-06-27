#!/usr/bin/env python3
"""
Test spécifique pour l'envoi d'emails et implémentation si nécessaire
"""

import sys
import os

# Ajouter le dossier parent au path pour importer l'app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_email_setup():
    """Vérifier la configuration email actuelle"""
    print("=== VÉRIFICATION DE LA CONFIGURATION EMAIL ===")
    
    try:
        from RetailShop import app
        
        # Vérifier si Flask-Mail est configuré
        email_settings = [
            'MAIL_SERVER',
            'MAIL_PORT', 
            'MAIL_USE_TLS',
            'MAIL_USE_SSL',
            'MAIL_USERNAME',
            'MAIL_PASSWORD'
        ]
        
        configured_settings = []
        for setting in email_settings:
            if setting in app.config:
                configured_settings.append(setting)
                print(f"✓ {setting} configuré")
            else:
                print(f"✗ {setting} non configuré")
        
        if len(configured_settings) == 0:
            print("❌ Aucune configuration email trouvée")
            return False
        elif len(configured_settings) < len(email_settings):
            print("⚠️  Configuration email partielle")
            return False
        else:
            print("✅ Configuration email complète")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def implement_email_functionality():
    """Implémenter la fonctionnalité d'envoi d'email si elle n'existe pas"""
    print("\n=== IMPLÉMENTATION DE LA FONCTIONNALITÉ EMAIL ===")
    
    # Vérifier si Flask-Mail est dans requirements.txt
    try:
        with open('/home/lelouch/Retail/requirements.txt', 'r') as f:
            requirements = f.read()
            if 'Flask-Mail' not in requirements:
                print("📝 Ajout de Flask-Mail aux requirements...")
                with open('/home/lelouch/Retail/requirements.txt', 'a') as f:
                    f.write('\nFlask-Mail==0.9.1\n')
                print("✅ Flask-Mail ajouté aux requirements")
            else:
                print("✅ Flask-Mail déjà dans requirements.txt")
    except Exception as e:
        print(f"❌ Erreur avec requirements.txt: {e}")
    
    # Créer un fichier de configuration email
    email_config = '''
# Configuration Email pour Flask-Mail
# Ajouter ces lignes à config.py ou __init__.py

from flask_mail import Mail

# Configuration Gmail (exemple)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'votre-email@gmail.com'  # À remplacer
MAIL_PASSWORD = 'votre-mot-de-passe-app'  # À remplacer
MAIL_DEFAULT_SENDER = 'votre-email@gmail.com'  # À remplacer

# Initialiser Flask-Mail
mail = Mail(app)
'''
    
    try:
        with open('/home/lelouch/Retail/email_config_template.py', 'w') as f:
            f.write(email_config)
        print("✅ Template de configuration email créé: email_config_template.py")
    except Exception as e:
        print(f"❌ Erreur création template: {e}")
    
    # Créer un utilitaire d'envoi d'email
    email_utils = '''"""
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
'''
    
    try:
        with open('/home/lelouch/Retail/RetailShop/email_utils.py', 'w') as f:
            f.write(email_utils)
        print("✅ Utilitaire email créé: RetailShop/email_utils.py")
    except Exception as e:
        print(f"❌ Erreur création utilitaire: {e}")

def create_email_templates():
    """Créer les templates d'emails"""
    print("\n=== CRÉATION DES TEMPLATES EMAIL ===")
    
    # Créer le dossier emails dans templates
    email_dir = '/home/lelouch/Retail/RetailShop/templates/emails'
    os.makedirs(email_dir, exist_ok=True)
    
    # Template de confirmation d'inscription
    registration_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Bienvenue sur RetailShop</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .footer { padding: 20px; text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bienvenue sur RetailShop !</h1>
        </div>
        <div class="content">
            <h2>Bonjour {{ user_name }},</h2>
            <p>Merci de vous être inscrit sur RetailShop ! Votre compte a été créé avec succès.</p>
            <p>Vous pouvez maintenant :</p>
            <ul>
                <li>Parcourir notre catalogue de produits</li>
                <li>Ajouter des articles à votre panier</li>
                <li>Passer des commandes en ligne</li>
            </ul>
            <p>Nous vous souhaitons une excellente expérience d'achat !</p>
        </div>
        <div class="footer">
            <p>L'équipe RetailShop</p>
        </div>
    </div>
</body>
</html>'''
    
    # Template de confirmation de commande
    order_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Confirmation de commande</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .footer { padding: 20px; text-align: center; color: #666; }
        .order-details { background: white; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Commande confirmée !</h1>
        </div>
        <div class="content">
            <h2>Bonjour {{ user_name }},</h2>
            <p>Nous avons bien reçu votre commande. Voici les détails :</p>
            <div class="order-details">
                <h3>Détails de la commande :</h3>
                <p><strong>Produit :</strong> {{ order_details.product_name }}</p>
                <p><strong>Quantité :</strong> {{ order_details.quantity }}</p>
                <p><strong>Prix :</strong> {{ order_details.price }}€</p>
                <p><strong>Livraison :</strong> {{ order_details.delivery_address }}</p>
            </div>
            <p>Votre commande sera traitée dans les plus brefs délais.</p>
        </div>
        <div class="footer">
            <p>Merci de votre confiance !</p>
            <p>L'équipe RetailShop</p>
        </div>
    </div>
</body>
</html>'''
    
    # Template de notification admin
    admin_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nouvelle commande</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #dc3545; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .order-details { background: white; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 Nouvelle commande reçue</h1>
        </div>
        <div class="content">
            <h2>Nouvelle commande à traiter</h2>
            <div class="order-details">
                <h3>Détails :</h3>
                <p><strong>Client :</strong> {{ order_details.customer_name }}</p>
                <p><strong>Email :</strong> {{ order_details.customer_email }}</p>
                <p><strong>Produit :</strong> {{ order_details.product_name }}</p>
                <p><strong>Quantité :</strong> {{ order_details.quantity }}</p>
                <p><strong>Prix :</strong> {{ order_details.price }}€</p>
                <p><strong>Adresse :</strong> {{ order_details.delivery_address }}</p>
                <p><strong>Date :</strong> {{ order_details.order_date }}</p>
            </div>
            <p>Connectez-vous à l'interface admin pour traiter cette commande.</p>
        </div>
    </div>
</body>
</html>'''
    
    try:
        with open(f'{email_dir}/registration_confirmation.html', 'w') as f:
            f.write(registration_template)
        print("✅ Template inscription créé")
        
        with open(f'{email_dir}/order_confirmation.html', 'w') as f:
            f.write(order_template)
        print("✅ Template commande créé")
        
        with open(f'{email_dir}/admin_order_notification.html', 'w') as f:
            f.write(admin_template)
        print("✅ Template notification admin créé")
        
    except Exception as e:
        print(f"❌ Erreur création templates: {e}")

def create_integration_guide():
    """Créer un guide d'intégration des emails"""
    guide = '''# Guide d'intégration des emails

## Étape 1: Installation
```bash
pip install Flask-Mail
```

## Étape 2: Configuration dans __init__.py
```python
from flask_mail import Mail

# Ajouter après la configuration de l'app
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'votre-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'votre-mot-de-passe-app'
app.config['MAIL_DEFAULT_SENDER'] = 'votre-email@gmail.com'
app.config['ADMIN_EMAIL'] = 'admin@retailshop.com'

mail = Mail(app)
```

## Étape 3: Décommenter l'import dans email_utils.py
```python
from RetailShop import mail  # Décommenter cette ligne
```

## Étape 4: Intégrer dans les routes

### Dans la route register (ligne ~129 de routes.py):
```python
# Après l'insertion en base
from RetailShop.email_utils import send_registration_confirmation
send_registration_confirmation(email, name)
```

### Dans la route de commande (ligne ~197 de routes.py):
```python
# Après l'insertion de la commande
from RetailShop.email_utils import send_order_confirmation, send_admin_notification

# Email au client
order_details = {
    'product_name': product_name,
    'quantity': quantity,
    'price': price,
    'delivery_address': order_place
}
send_order_confirmation(user_email, user_name, order_details)

# Notification admin
send_admin_notification(order_details)
```

## Configuration Gmail
1. Activer l'authentification à 2 facteurs
2. Générer un mot de passe d'application
3. Utiliser ce mot de passe dans MAIL_PASSWORD

## Test
Utilisez le script test_email.py pour tester l'envoi.
'''
    
    try:
        with open('/home/lelouch/Retail/GUIDE_EMAIL_INTEGRATION.md', 'w') as f:
            f.write(guide)
        print("✅ Guide d'intégration créé: GUIDE_EMAIL_INTEGRATION.md")
    except Exception as e:
        print(f"❌ Erreur création guide: {e}")

if __name__ == "__main__":
    print("🔧 CONFIGURATION ET IMPLÉMENTATION DES EMAILS")
    print("=" * 60)
    
    # Vérifier la configuration actuelle
    email_configured = check_email_setup()
    
    if not email_configured:
        print("\n🛠️  IMPLÉMENTATION DE LA FONCTIONNALITÉ EMAIL...")
        implement_email_functionality()
        create_email_templates()
        create_integration_guide()
        
        print("\n" + "=" * 60)
        print("📧 IMPLÉMENTATION TERMINÉE !")
        print("📋 Actions à effectuer :")
        print("1. Installer Flask-Mail: pip install Flask-Mail")
        print("2. Configurer les paramètres email dans __init__.py")
        print("3. Décommenter l'import dans email_utils.py")
        print("4. Intégrer les appels d'envoi dans les routes")
        print("5. Consulter GUIDE_EMAIL_INTEGRATION.md pour les détails")
    else:
        print("\n✅ Configuration email déjà présente !")
