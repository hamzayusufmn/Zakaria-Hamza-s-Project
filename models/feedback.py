# models/feedback.py
# Database model for customer feedback
# Author: Zakaria
# Created: April 2025

from extensions import db  # Import from extensions instead of app
from datetime import datetime

class Feedback(db.Model):
    """Model for storing customer feedback submissions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 star rating
    visited_on = db.Column(db.Date)
    is_read = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback from {self.name} on {self.submitted_at.strftime("%Y-%m-%d")}>'
    # return feedback and shows user time in year-month-day format