# init_db.py
# Script to initialize the database with sample data
# Author: Zakaria
# Created: April 2025

from app import app
from extensions import db  # Import db from extensions instead of app
from models.user import User
from models.menu import MenuItem, Category
from models.hours import Hours
from utils.admin_helpers import create_admin_user, initialize_menu_categories, initialize_hours
import os

def init_database():
    """Initialize the database with tables and sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Rest of the function remains the same