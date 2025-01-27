from flask import Blueprint, jsonify, request
from PIL import Image, ImageOps, ImageFilter
import os

filtros_blueprint = Blueprint('filtros', __name__)

UPLOAD_FOLDER = './img'

def aplicar_filtro(imagen, filtro='blanco_negro'):
    if filtro == 'blanco_negro':
        return imagen.convert('L')
    elif filtro == 'sepia':
        sepia = ImageOps.colorize(ImageOps.grayscale(imagen), '#704214', '#fff8dc')
        return sepia
    elif filtro == 'borroso':
        return imagen.filter(ImageFilter.GaussianBlur(5))
    elif filtro == 'nitidez':  # Filtro de nitidez
        return imagen.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    elif filtro == 'invertir':  # Filtro de invertir colores
        # Convertir la imagen a RGB si no lo es ya
        if imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')
        # Invertir los colores
        return ImageOps.invert(imagen)
    return imagen

@filtros_blueprint.route('/', methods=['POST'], strict_slashes=False)
def aplicar_filtro_endpoint():
    try:
        # Verificar si se ha enviado un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó un archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'El archivo no tiene un nombre válido'}), 400
        
        # Obtener el filtro (default blanco y negro)
        filtro = request.form.get('filtro', 'blanco_negro')

        # Asegurar que la carpeta existe
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Guardar el archivo original temporalmente
        original_filename = file.filename
        original_path = os.path.join(UPLOAD_FOLDER, original_filename)
        file.save(original_path)

        # Abrir la imagen y aplicar el filtro
        with Image.open(original_path) as img:
            imagen_filtrada = aplicar_filtro(img, filtro)

            # Crear el nombre del archivo filtrado
            filename_without_ext, ext = os.path.splitext(original_filename)
            filtered_filename = f"{filename_without_ext}_{filtro}{ext}"
            filtered_path = os.path.join(UPLOAD_FOLDER, filtered_filename)

            # Guardar la imagen filtrada
            imagen_filtrada.save(filtered_path)

        # Eliminar el archivo original
        os.remove(original_path)

        return jsonify({
            'message': 'Filtro aplicado exitosamente',
            'original_filename': original_filename,
            'filtered_filename': filtered_filename,
            'filepath': filtered_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
