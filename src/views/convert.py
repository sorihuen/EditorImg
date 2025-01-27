from flask import Blueprint, jsonify, request
from PIL import Image
import os

convert_blueprint = Blueprint('convert', __name__)

UPLOAD_FOLDER = './img'

@convert_blueprint.route('/', methods=['POST'], strict_slashes=False)
def convert_image():
    try:
        print(request.files)  # Imprime los archivos recibidos
        file = request.files.get('file')
        format_type = request.form.get('format')  # Obtener el formato deseado

        if not file:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400

        if file.filename == '':
            return jsonify({'error': 'El archivo no tiene un nombre válido'}), 400

        # Normalizar el formato ingresado a minúsculas
        if not format_type:
            return jsonify({'error': 'No se especificó un formato de conversión'}), 400
        format_type = format_type.lower()

        # Lista de formatos soportados
        supported_formats = ['jpg', 'png', 'webp', 'jpeg', 'bmp', 'tiff', 'gif']

        if format_type not in supported_formats:
            return jsonify({
                'error': f'Formato de conversión no soportado. Usa uno de los siguientes: {", ".join(supported_formats)}.'
            }), 400

        # Pillow espera 'JPEG' en lugar de 'JPG'
        if format_type == 'jpg':
            format_type = 'jpeg'

        # Guardar el archivo original
        original_filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        # Convertir la imagen al formato deseado
        with Image.open(original_path) as img:
            img = img.convert('RGB') if format_type != 'gif' else img  # Convertir a RGB excepto para GIF
            new_filename = os.path.splitext(original_filename)[0] + f'.{format_type}'
            new_path = os.path.join(UPLOAD_FOLDER, new_filename)

            # Guardar como GIF si es el formato solicitado
            if format_type == 'gif':
                img.save(new_path, save_all=True)  # `save_all=True` conserva marcos animados si existen
            else:
                img.save(new_path, format_type.upper())  # Guardar en el formato deseado

            os.remove(original_path)  # Eliminar el archivo original
        return jsonify({
            'original_filename': original_filename,
            'converted_filename': new_filename,
            'message': f'La imagen fue convertida a {format_type.upper()} exitosamente',
            'filepath': new_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


