# models/menu.py
# Database models for menu items and categories
# Author: Zakaria
# Created: April 2025

from app import db
from datetime import datetime

class Category(db.Model):
    """Model for food categories (appetizers, entrees, desserts)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    display_order = db.Column(db.Integer, default=0)
    items = db.relationship('MenuItem', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class MenuItem(db.Model):
    """Model for individual food items on the menu"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(255))
    
    # Dietary flags
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    is_gluten_free = db.Column(db.Boolean, default=False)
    contains_nuts = db.Column(db.Boolean, default=False)
    
    # Foreign key to category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'