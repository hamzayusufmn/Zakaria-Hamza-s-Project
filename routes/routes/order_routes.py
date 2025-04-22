# routes/order_routes.py
# Routes for online ordering system
# Author: Zakaria
# Created: April 2025

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models.menu import MenuItem, Category
from models.order import Order, OrderItem
from app import db
from datetime import datetime, timedelta

# Create blueprint
order_bp = Blueprint('order', __name__, url_prefix='/order')

@order_bp.route('/')
def order_page():
    """Display the ordering page"""
    # Get all menu categories and items
    categories = Category.query.order_by(Category.display_order).all()
    
    # Calculate available pickup times (30 min intervals for next 3 hours)
    current_time = datetime.now()
    pickup_times = []
    
    # Start 30 minutes from now, round to next 30 min interval
    start_time = current_time + timedelta(minutes=30)
    minutes_to_add = 30 - (start_time.minute % 30)
    start_time = start_time + timedelta(minutes=minutes_to_add)
    
    # Generate time slots for 3 hours
    for i in range(6):  # 6 slots of 30 minutes = 3 hours
        pickup_time = start_time + timedelta(minutes=i*30)
        if pickup_time.hour < 22:  # Don't show times after 10 PM
            time_str = pickup_time.strftime("%I:%M %p")
            pickup_times.append(time_str)
    
    return render_template('order.html', 
                          categories=categories, 
                          pickup_times=pickup_times)

@order_bp.route('/submit', methods=['POST'])
def submit_order():
    """Process the order submission"""
    if request.method == 'POST':
        # Get customer information
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        pickup_time_str = request.form.get('pickup_time')
        special_instructions = request.form.get('special_instructions')
        
        # Parse pickup time string to datetime
        pickup_time = datetime.strptime(pickup_time_str, "%I:%M %p")
        pickup_datetime = datetime.now().replace(
            hour=pickup_time.hour, 
            minute=pickup_time.minute,
            second=0,
            microsecond=0
        )
        
        # Create new order
        new_order = Order(
            name=name,
            phone=phone,
            email=email,
            pickup_time=pickup_datetime,
            special_instructions=special_instructions,
            order_total=0,  # Will calculate below
            status='pending'
        )
        
        db.session.add(new_order)
        db.session.flush()  # Get order ID without committing
        
        # Process order items
        order_total = 0
        
        # Get item IDs and quantities from form
        for key, value in request.form.items():
            if key.startswith('item_'):
                item_id = int(key.split('_')[1])
                quantity = int(value)
                
                if quantity > 0:
                    # Get menu item
                    menu_item = MenuItem.query.get(item_id)
                    
                    if menu_item:
                        # Create order item
                        order_item = OrderItem(
                            order_id=new_order.id,
                            menu_item_id=item_id,
                            quantity=quantity,
                            item_price=menu_item.price
                        )
                        
                        # Add to total
                        item_total = menu_item.price * quantity
                        order_total += item_total
                        
                        db.session.add(order_item)
        
        # Update order total
        new_order.order_total = order_total
        
        # Commit all changes
        db.session.commit()
        
        flash('Your order has been submitted successfully!', 'success')
        return redirect(url_for('order.confirmation', order_id=new_order.id))
    
    return redirect(url_for('order.order_page'))

@order_bp.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    """Display order confirmation page"""
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)