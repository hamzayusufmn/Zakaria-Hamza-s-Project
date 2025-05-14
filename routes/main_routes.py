# routes/main_routes.py
# Routes for main pages (home, contact, about)
# Author: Zakaria
# Created: April 2025

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.hours import Hours
from models.menu import MenuItem, Category
from models.feedback import Feedback  # Import the Feedback model
from extensions import db  # Import db
from datetime import datetime  # Import datetime

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
        try:
            # Get all the form data
            name = request.form['name']
            email = request.form['email']
            phone = request.form.get('phone', '')  # Optional
            rating = int(request.form['rating'])
            visited_on = datetime.strptime(request.form['visited_on'], '%Y-%m-%d').date()
            message = request.form['message']

            # Create new feedback entry
            new_feedback = Feedback(
                name=name,
                email=email,
                phone=phone,
                rating=rating,
                visited_on=visited_on,
                message=message
            )
            
            # Save to database
            db.session.add(new_feedback)
            db.session.commit()
            
            # Redirect to confirmation page
            return redirect(url_for('main.feedback_confirmation'))
            
        except Exception as e:
            # If there's an error, roll back the database session and show error
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('main.feedback'))

    # For GET requests, just render the form
    # You can get the order_id from query parameters if needed
    order_id = request.args.get('order_id')
    return render_template('feedback.html', order_id=order_id)

@main_bp.route('/feedback/confirmation')
def feedback_confirmation():
    return render_template('feedback_confirmation.html')

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

@main_bp.route('/cart/clear', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared.', 'warning')
    return redirect(url_for('main.view_cart'))