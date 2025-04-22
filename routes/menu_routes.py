# routes/menu_routes.py
# Routes for menu display and filtering
# Author: Zakaria
# Created: April 2025

from flask import Blueprint, render_template, request
from models.menu import MenuItem, Category
from sqlalchemy import asc

# Create blueprint
menu_bp = Blueprint('menu', __name__, url_prefix='/menu')

@menu_bp.route('/')
def menu_display():
    """Display the full menu with categories"""
    # Get all categories ordered by display_order
    categories = Category.query.order_by(asc(Category.display_order)).all()
    
    # Handle dietary restriction filters
    is_vegetarian = request.args.get('vegetarian') == 'true'
    is_vegan = request.args.get('vegan') == 'true'
    is_gluten_free = request.args.get('gluten_free') == 'true'
    is_nut_free = request.args.get('nut_free') == 'true'
    
    # Create a dictionary to store filtered items by category
    filtered_items = {}
    
    for category in categories:
        # Start with all items in this category
        query = MenuItem.query.filter_by(category_id=category.id)
        
        # Apply filters if any are selected
        if is_vegetarian:
            query = query.filter_by(is_vegetarian=True)
        if is_vegan:
            query = query.filter_by(is_vegan=True)
        if is_gluten_free:
            query = query.filter_by(is_gluten_free=True)
        if is_nut_free:
            query = query.filter_by(contains_nuts=False)
            
        # Store the filtered items
        filtered_items[category.id] = query.all()
    
    return render_template('menu.html', 
                           categories=categories, 
                           filtered_items=filtered_items,
                           filters={
                               'vegetarian': is_vegetarian,
                               'vegan': is_vegan,
                               'gluten_free': is_gluten_free,
                               'nut_free': is_nut_free
                           })

@menu_bp.route('/<int:category_id>')
def category_display(category_id):
    """Display items from a specific category"""
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)