
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
