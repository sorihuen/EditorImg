# change_size.py

from flask import Blueprint, jsonify, request
from PIL import Image
import os

resize_blueprint = Blueprint('resize', __name__)

UPLOAD_FOLDER = './img'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def change_size(image, scale_factor=0.5):
    """
    Change the size of the image based on the given scale factor.
    The scale factor should be a float (e.g., 0.5 to reduce the size by half, 2.0 to double the size).
    """
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    return image.resize(new_size)


@resize_blueprint.route('/', methods=['POST'], strict_slashes=False)
def resize_endpoint():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file name provided'}), 400

        # Get the scale factor from the form data (default is 0.5)
        scale_factor_str = request.form.get('scale_factor', '0.5')  # Default to '0.5' if not provided
        # Check if scale_factor is a valid number
        try:
            scale_factor = float(scale_factor_str)
        except ValueError:
            return jsonify({'error': 'Invalid scale_factor value'}), 400

        # Save the file temporarily
        original_filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        # Open the image and apply the resize
        with Image.open(original_path) as img:
            resized_image = change_size(img, scale_factor)

            # Create a new name for the resized file
            filename_without_ext, ext = os.path.splitext(original_filename)
            resized_filename = f"{filename_without_ext}_resized{ext}"
            resized_path = os.path.join(UPLOAD_FOLDER, resized_filename)

            # Save the resized image
            resized_image.save(resized_path)

        # Remove the original file
        os.remove(original_path)

        return jsonify({
            'message': 'Image resized successfully',
            'original_filename': original_filename,
            'resized_filename': resized_filename,
            'filepath': resized_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
