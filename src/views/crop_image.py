# crop_image.py

from flask import Blueprint, jsonify, request
from PIL import Image
import os

crop_blueprint = Blueprint('crop', __name__)  # Renombrado a 'crop_blueprint'

UPLOAD_FOLDER = './img'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def crop(image, margin=50, crop_width=False, crop_height=False):
    """
    Crop the image based on the provided margin or only from one side.
    If crop_width or crop_height are True, it will crop only in that direction.
    """
    if crop_width:
        # Crop only the width (left and right)
        image = image.crop((margin, 0, image.width - margin, image.height))
    elif crop_height:
        # Crop only the height (top and bottom)
        image = image.crop((0, margin, image.width, image.height - margin))
    else:
        # Crop from all four edges (top, bottom, left, right)
        image = image.crop((margin, margin, image.width - margin, image.height - margin))
    
    return image

@crop_blueprint.route('/', methods=['POST'], strict_slashes=False)
def crop_endpoint():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file name provided'}), 400

        # Get crop parameters
        margin = int(request.form.get('margin', 50))  # Default margin 50
        crop_width = request.form.get('crop_width', 'false').lower() == 'true'
        crop_height = request.form.get('crop_height', 'false').lower() == 'true'

        # Save the file temporarily
        original_filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        # Open the image and apply the crop
        with Image.open(original_path) as img:
            cropped_image = crop(img, margin, crop_width, crop_height)

            # Create filename for cropped image
            filename_without_ext, ext = os.path.splitext(original_filename)
            cropped_filename = f"{filename_without_ext}_cropped{ext}"
            cropped_path = os.path.join(UPLOAD_FOLDER, cropped_filename)

            # Save the cropped image
            cropped_image.save(cropped_path)

        # Remove the original file
        os.remove(original_path)

        return jsonify({
            'message': 'Image cropped successfully',
            'original_filename': original_filename,
            'cropped_filename': cropped_filename,
            'filepath': cropped_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
