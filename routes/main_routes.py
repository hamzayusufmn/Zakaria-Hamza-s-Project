# routes/main_routes.py
# Routes for main pages (home, contact, about)
# Author: Zakaria
# Created: April 2025

from flask import Blueprint, render_template, request
from models.hours import Hours

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Route for homepage"""
    # Get restaurant hours to display on homepage
    hours = Hours.query.filter_by(is_special=False).all()
    return render_template('index.html', hours=hours)

@main_bp.route('/contact')
def contact():
    """Route for contact page"""
    hours = Hours.query.filter_by(is_special=False).all()
    return render_template('contact.html', hours=hours)

@main_bp.route('/about')
def about():
    """Route for about page"""
    return render_template('about.html')

@main_bp.route('/gallery')
def gallery():
    """Route for photo gallery"""
    return render_template('gallery.html')