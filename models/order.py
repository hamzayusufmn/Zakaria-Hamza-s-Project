# models/order.py
# Database models for online orders
# Author: Zakaria
# Created: April 2025

from app import db
from datetime import datetime

class Order(db.Model):
    """Model for customer orders"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False)
    order_total = db.Column(db.Float, nullable=False)
    special_instructions = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order #{self.id} - {self.name} - {self.status}>'

class OrderItem(db.Model):
    """Model for individual items in an order"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item_price = db.Column(db.Float, nullable=False)  # Price at time of order
    special_requests = db.Column(db.Text)
    
    # Reference to the menu item
    menu_item = db.relationship('MenuItem')
    
    def __repr__(self):
        return f'<OrderItem {self.menu_item.name} x{self.quantity}>'