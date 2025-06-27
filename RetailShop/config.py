"""
Configuration file for the RetailShop application
"""
import os

# Get the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # MySQL configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '127.0.0.1'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'webapp'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'motdepassefort'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'shoptubedb'
    MYSQL_CURSORCLASS = 'DictCursor'

    # Upload configuration
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static', 'image', 'product')
