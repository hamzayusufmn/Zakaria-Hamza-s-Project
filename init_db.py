# init_db.py
# Script to initialize the database with sample data
# Author: Zakaria
# Created: April 2025

from app import app, db
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
        
        # Create admin user
        admin_username = app.config.get('ADMIN_USERNAME', 'admin')
        admin_password = app.config.get('ADMIN_PASSWORD', 'password')
        create_admin_user(admin_username, admin_password)
        
        # Initialize menu categories
        initialize_menu_categories()
        
        # Initialize restaurant hours
        initialize_hours()
        
        # Add sample menu items
        if MenuItem.query.count() == 0:
            # Get categories
            appetizers = Category.query.filter_by(name='Appetizers').first()
            entrees = Category.query.filter_by(name='Entrees').first()
            desserts = Category.query.filter_by(name='Desserts').first()
            
            # Sample items
            items = [
                {
                    'name': 'Hummus',
                    'description': 'Creamy chickpea dip served with warm pita bread.',
                    'price': 8.99,
                    'is_vegetarian': True,
                    'is_vegan': True,
                    'is_gluten_free': False,
                    'contains_nuts': False,
                    'category_id': appetizers.id if appetizers else 1
                },
                {
                    'name': 'Falafel',
                    'description': 'Crispy chickpea fritters served with tahini sauce.',
                    'price': 9.99,
                    'is_vegetarian': True,
                    'is_vegan': True,
                    'is_gluten_free': False,
                    'contains_nuts': False,
                    'category_id': appetizers.id if appetizers else 1
                },
                {
                    'name': 'Shawarma Plate',
                    'description': 'Marinated meat, slowly roasted and served with rice and salad.',
                    'price': 16.99,
                    'is_vegetarian': False,
                    'is_vegan': False,
                    'is_gluten_free': True,
                    'contains_nuts': False,
                    'category_id': entrees.id if entrees else 3
                },
                {
                    'name': 'Baklava',
                    'description': 'Flaky pastry layered with honey and chopped nuts.',
                    'price': 6.99,
                    'is_vegetarian': True,
                    'is_vegan': False,
                    'is_gluten_free': False,
                    'contains_nuts': True,
                    'category_id': desserts.id if desserts else 5
                }
            ]
            
            for item_data in items:
                item = MenuItem(**item_data)
                db.session.add(item)
            
            db.session.commit()
            print("Sample menu items added successfully!")
        
        print("Database initialization complete!")

if __name__ == "__main__":
    init_database()

    