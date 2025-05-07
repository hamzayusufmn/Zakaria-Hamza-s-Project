# routes/admin_routes.py
# Routes for admin dashboard and authentication
# Author: Zakaria
# Created: April 2025

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.menu import MenuItem, Category
from models.feedback import Feedback
from models.order import Order
from datetime import datetime
from extensions import db  # Import from extensions instead of app
from functools import wraps

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login route"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = user.username
            
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Admin logout route"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_required
def dashboard():
    """Admin dashboard route"""
    # Get counts for dashboard statistics
    menu_count = MenuItem.query.count()
    unread_feedback = Feedback.query.filter_by(is_read=False).count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
                          menu_count=menu_count,
                          unread_feedback=unread_feedback,
                          pending_orders=pending_orders)

@admin_bp.route('/menu')
@admin_required
def menu_management():
    """Menu management route"""
    categories = Category.query.all()
    menu_items = MenuItem.query.all()
    return render_template('admin/menu_management.html', 
                          categories=categories,
                          menu_items=menu_items)

@admin_bp.route('/feedback')
@admin_required
def feedback_management():
    """Feedback management route"""
    feedback = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template('admin/feedback_management.html', feedback=feedback)

@admin_bp.route('/orders')
@admin_required
def order_management():
    """Order management route"""
    status_filter = request.args.get('status', '')
    
    if status_filter:
        orders = Order.query.filter_by(status=status_filter).order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        
    return render_template('admin/order_management.html', orders=orders, current_filter=status_filter)