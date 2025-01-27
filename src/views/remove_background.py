from flask import Blueprint, jsonify, request
from rembg import remove
import os

remove_bg_blueprint = Blueprint('remove_bg', __name__)

UPLOAD_FOLDER = './img'

@remove_bg_blueprint.route('/', methods=['POST'], strict_slashes=False)
def remove_background():
    """
    Remove Background from an Image
    ---
    tags:
      - Background Removal
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The image file from which the background will be removed.
    responses:
      200:
        description: Background removed successfully
        schema:
          type: object
          properties:
            original_filename:
              type: string
              description: The original name of the uploaded file.
            new_filename:
              type: string
              description: The name of the new file without the background.
            message:
              type: string
              description: Success message.
            filepath:
              type: string
              description: Path to the file with the background removed.
      400:
        description: Bad request, invalid or missing input file.
      500:
        description: Internal server error.
    """
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400

        if file.filename == '':
            return jsonify({'error': 'El archivo no tiene un nombre válido'}), 400

        # Guardar el archivo original
        original_filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        # Leer el archivo y eliminar el fondo
        with open(original_path, 'rb') as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)  # Remover fondo usando rembg

        # Guardar la nueva imagen sin fondo
        new_filename = os.path.splitext(original_filename)[0] + '_no_bg.png'
        new_path = os.path.join(UPLOAD_FOLDER, new_filename)
        with open(new_path, 'wb') as output_file:
            output_file.write(output_data)

        os.remove(original_path)  # Eliminar el archivo original

        return jsonify({
            'original_filename': original_filename,
            'new_filename': new_filename,
            'message': 'El fondo fue eliminado exitosamente',
            'filepath': new_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
