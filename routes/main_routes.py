# routes/main_routes.py
# Routes for main pages (home, contact, about)
# Author: Zakaria
# Created: April 2025

from flask import Blueprint, render_template, request
from models.hours import Hours
from flask import session, render_template, redirect, url_for, flash, request
from models.menu import MenuItem, Category


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

@main_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Handle form submission later
        pass
    return render_template('feedback.html')
    # added this so feedback.html can be rendered
    # without any issues flask coudlnt find it.

@main_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0.0
    for id_str, qty in cart.items():
        item = MenuItem.query.get(int(id_str))
        if item:
            subtotal = item.price * qty
            cart_items.append({'item': item, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', cart_items=cart_items, total=total)

@main_bp.route('/cart/add/<int:menu_item_id>', methods=['POST'])
def add_to_cart(menu_item_id):
    cart = session.get('cart', {})
    cart[str(menu_item_id)] = cart.get(str(menu_item_id), 0) + 1
    session['cart'] = cart
    flash('Added to cart!', 'success')
    return redirect(request.referrer or url_for('menu.menu_display'))

@main_bp.route('/cart/remove/<int:menu_item_id>', methods=['POST'])
def remove_from_cart(menu_item_id):
    cart = session.get('cart', {})
    cart.pop(str(menu_item_id), None)
    session['cart'] = cart
    flash('Removed from cart.', 'info')
    return redirect(request.referrer or url_for('main.view_cart'))

@main_bp.route('/cart/clear', methods=['POST']) # hy- this wasnt working when i was testing remove all from cart. forgot to add this, mustve been triggered by a get request.
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared.', 'warning')
    return redirect(url_for('main.view_cart'))
