# config.py
# Configuration settings for the Flask application
# Author: Zakaria
# Created: April 2025

import os

# Base directory of application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for sessions and CSRF protection
SECRET_KEY = 'generate-a-strong-secret-key'  # Change this in production!

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'restaurant.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Upload folder for menu images and gallery
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload size

# Admin user credentials - move to env variables in production
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'  # Change this in production!
