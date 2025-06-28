# Guide d'intégration des emails

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
