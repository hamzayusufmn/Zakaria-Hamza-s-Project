# utils/image_helpers.py
# Helper functions for image handling
# Author: Zakaria
# Created: April 2025

import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file, subfolder='uploads'):
    """Save uploaded image and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Create a unique filename to prevent overwriting
        base_name, extension = os.path.splitext(filename)
        import uuid
        unique_filename = f"{base_name}_{uuid.uuid4().hex[:8]}{extension}"
        
        # Ensure upload folder exists
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # Return the path relative to static folder
        return os.path.join('images', 'uploads', subfolder, unique_filename)
    
    return None

def delete_image(image_path):
    """Delete an image from the filesystem"""
    if image_path:
        # Convert relative path to absolute path
        full_path = os.path.join(current_app.static_folder, image_path)
        
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    
    return False