# models/hours.py
# Database model for restaurant operating hours
# Author: Zakaria
# Created: April 2025

from extensions import db  # Import from extensions instead of app

class Hours(db.Model):
    """Model for restaurant operating hours"""
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.String(10), nullable=False)  # Monday, Tuesday, etc.
    open_time = db.Column(db.String(10), nullable=False)  # Format: HH:MM AM/PM
    close_time = db.Column(db.String(10), nullable=False)  # Format: HH:MM AM/PM
    is_closed = db.Column(db.Boolean, default=False)  # For days restaurant is closed
    is_special = db.Column(db.Boolean, default=False)  # For holiday hours
    special_date = db.Column(db.Date)  # For specific dates with special hours
    
    def __repr__(self):
        if self.is_closed:
            return f'<Hours {self.day_of_week}: Closed>'
        return f'<Hours {self.day_of_week}: {self.open_time} - {self.close_time}>'