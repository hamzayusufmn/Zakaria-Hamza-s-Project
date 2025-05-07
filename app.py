# app.py
# Main application file that initializes Flask and configures the app
# Author: Zakaria
# Created: April 2025

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from extensions import db  # Import db from extensions instead

# Create and configure the app
app = Flask(__name__)
app.config.from_object('config')

# Initialize database with app
db.init_app(app)  # Changed from db = SQLAlchemy(app)

# Set up CSRF protection for forms
csrf = CSRFProtect(app)

# Import routes after db is defined to avoid circular imports
from routes.main_routes import main_bp
from routes.menu_routes import menu_bp
from routes.admin_routes import admin_bp
from routes.order_routes import order_bp

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(order_bp)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Run the app if executed directly
if __name__ == '__main__':
    app.run(debug=True)