from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

def create_routes(app):
    # Usamos la carpeta img para guardar las imágenes
    UPLOAD_FOLDER = './img'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Asegúrate de que la carpeta exista

    @app.route('/upload', methods=['POST'])
    def upload():
        print("Inicio del proceso de carga")  # Mensaje inicial
        try:
            # Obtener el archivo enviado
            file = request.files.get('file')
            if not file:
                print("Error: No se proporcionó un archivo")  # Mensaje de error
                return jsonify({'error': 'No se proporcionó un archivo'}), 400

            # Validar que el archivo tiene nombre
            if file.filename == '':
                print("Error: El archivo no tiene un nombre válido")  # Mensaje de error
                return jsonify({'error': 'El archivo no tiene un nombre válido'}), 400

            # Guardar el archivo original
            original_filename = file.filename
            original_path = os.path.join(UPLOAD_FOLDER, original_filename)
            file.save(original_path)

            # Confirmamos que el archivo se guardó correctamente
            print(f'Archivo guardado en: {original_path}')

            # Verificar si el archivo es PNG o JPEG/JPE
            if original_filename.lower().endswith(('.png', '.jpeg', '.jpg', '.jpe')):
                print(f'Archivo válido para conversión: {original_filename}')  # Mensaje de validación
                try:
                    # Abrir la imagen usando Pillow
                    with Image.open(original_path) as img:
                        print("Imagen abierta exitosamente")  # Mensaje de éxito al abrir imagen
                        # Convertir la imagen a RGB (necesario para JPG)
                        img = img.convert('RGB')

                        # Cambiar extensión y guardar como JPG
                        new_filename = os.path.splitext(original_filename)[0] + '.jpg'
                        new_path = os.path.join(UPLOAD_FOLDER, new_filename)

                        # Guardar la nueva imagen
                        img.save(new_path, 'JPEG')
                        print(f'Imagen convertida y guardada en: {new_path}')  # Mensaje de éxito al guardar

                    # Eliminar la imagen original si ya no es necesaria
                    os.remove(original_path)
                    print(f'Archivo original eliminado: {original_path}')  # Mensaje de eliminación

                    # Responder con los datos de la nueva imagen
                    return jsonify({
                        'original_filename': original_filename,
                        'converted_filename': new_filename,
                        'message': 'La imagen fue convertida a JPG exitosamente',
                        'filepath': new_path
                    }), 200

                except Exception as e:
                    print(f'Error al convertir la imagen: {str(e)}')  # Mensaje de error específico
                    return jsonify({'error': f'Error al convertir la imagen: {str(e)}'}), 500
            
            else:
                print("Error: Formato de archivo no soportado")  # Mensaje de error por formato no soportado
                return jsonify({'error': 'Formato de archivo no soportado. Solo se aceptan PNG, JPEG o JPE.'}), 400

        except Exception as e:
            print(f'Error general: {str(e)}')  # Mensaje de error general
            return jsonify({'error': str(e)}), 500

create_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
