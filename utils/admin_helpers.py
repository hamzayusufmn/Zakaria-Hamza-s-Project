# utils/admin_helpers.py
# Helper functions for admin operations
# Author: Zakaria
# Created: April 2025

from app import db
from models.user import User
from models.menu import MenuItem, Category
from models.hours import Hours
from werkzeug.security import generate_password_hash
import os

def create_admin_user(username, password, is_admin=True):
    """Create an admin user if one doesn't exist"""
    user = User.query.filter_by(username=username).first()
    
    if not user:
        user = User(username=username, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True
    return False

def initialize_menu_categories():
    """Create default menu categories if none exist"""
    if Category.query.count() == 0:
        categories = [
            {'name': 'Appetizers', 'description': 'Start your meal with these delicious options', 'display_order': 1},
            {'name': 'Salads', 'description': 'Fresh and healthy options', 'display_order': 2},
            {'name': 'Entrees', 'description': 'Main course dishes', 'display_order': 3},
            {'name': 'Sides', 'description': 'Perfect accompaniments', 'display_order': 4},
            {'name': 'Desserts', 'description': 'Sweet treats to finish your meal', 'display_order': 5},
            {'name': 'Beverages', 'description': 'Refreshing drinks', 'display_order': 6}
        ]
        
        for cat in categories:
            category = Category(**cat)
            db.session.add(category)
        
        db.session.commit()
        return True
    return False

def initialize_hours():
    """Create default restaurant hours if none exist"""
    if Hours.query.count() == 0:
        hours = [
            {'day_of_week': 'Monday', 'open_time': '11:00 AM', 'close_time': '9:00 PM', 'is_closed': False},
            {'day_of_week': 'Tuesday', 'open_time': '11:00 AM', 'close_time': '9:00 PM', 'is_closed': False},
            {'day_of_week': 'Wednesday', 'open_time': '11:00 AM', 'close_time': '9:00 PM', 'is_closed': False},
            {'day_of_week': 'Thursday', 'open_time': '11:00 AM', 'close_time': '9:00 PM', 'is_closed': False},
            {'day_of_week': 'Friday', 'open_time': '11:00 AM', 'close_time': '10:00 PM', 'is_closed': False},
            {'day_of_week': 'Saturday', 'open_time': '11:00 AM', 'close_time': '10:00 PM', 'is_closed': False},
            {'day_of_week': 'Sunday', 'open_time': '12:00 PM', 'close_time': '8:00 PM', 'is_closed': False}
        ]
        
        for h in hours:
            hour = Hours(**h)
            db.session.add(hour)
        
        db.session.commit()
        return True
    return False