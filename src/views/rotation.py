from flask import Blueprint, jsonify, request
from PIL import Image
import os

rotate_blueprint = Blueprint('rotate', __name__)

UPLOAD_FOLDER = './img'

@rotate_blueprint.route('/', methods=['POST'])
def rotate_image():
    try:
        # Debugging: imprimir lo que recibimos
        # print("Files received:", request.files)
        # print("Form data received:", request.form)
        
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
