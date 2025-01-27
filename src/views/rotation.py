from flask import Blueprint, jsonify, request
from PIL import Image
import os

rotate_blueprint = Blueprint('rotate', __name__)

UPLOAD_FOLDER = './img'

@rotate_blueprint.route('/', methods=['POST'])
def rotate_image():
    """
    Rotate an Image
    ---
    tags:
      - Image Manipulation
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file to be rotated.
      - name: angle
        in: formData
        type: number
        required: false
        description: The angle to rotate the image (default is 90 degrees).
    responses:
      200:
        description: Image rotated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message.
            original_filename:
              type: string
              description: The original name of the uploaded file.
            rotated_filename:
              type: string
              description: The name of the rotated file.
            angle:
              type: number
              description: The angle used for rotation.
            filepath:
              type: string
              description: Path to the rotated file.
      400:
        description: Bad request, invalid or missing input file.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message.
            files_received:
              type: array
              items:
                type: string
              description: List of file keys received in the request.
            form_data:
              type: object
              additionalProperties:
                type: string
              description: The form data received in the request.
      500:
        description: Internal server error.
    """
    
    try:

        if 'file' not in request.files:
            return jsonify({
                'error': 'No se proporcionó un archivo',
                'files_received': list(request.files.keys()),
                'form_data': dict(request.form)
            }), 400
        
        # Obtener el archivo y asegurarse de que no esté vacío
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'El archivo no tiene un nombre válido'}), 400
        
        # Obtener el ángulo de rotación (default 90 grados)
        angle = request.form.get('angle', 90, type=float)
        
        # Asegurar que la carpeta existe
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Guardar el archivo original temporalmente
        original_filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        # Abrir y rotar la imagen
        with Image.open(original_path) as img:
            # Rotar la imagen manteniendo el formato original
            rotated_img = img.rotate(angle, expand=True)
            
            # Crear el nombre del archivo rotado
            filename_without_ext, ext = os.path.splitext(original_filename)
            rotated_filename = f"{filename_without_ext}_rotated{ext}"
            rotated_path = os.path.join(UPLOAD_FOLDER, rotated_filename)
            
            # Guardar la imagen rotada
            rotated_img.save(rotated_path, quality=95)

        # Eliminar el archivo original
        os.remove(original_path)

        return jsonify({
            'message': 'Imagen rotada exitosamente',
            'original_filename': original_filename,
            'rotated_filename': rotated_filename,
            'angle': angle,
            'filepath': rotated_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
