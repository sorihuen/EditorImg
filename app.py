from flask import Flask, request, jsonify
from PIL import Image, ImageOps, ImageFilter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Crea carpetas para imágenes si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"message": "API de procesamiento de imágenes con Flask y Docker"})

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "El nombre del archivo está vacío"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Aquí puedes integrar tus funciones de procesamiento
    operacion = request.form.get('operacion', 'cambiar_tamaño')
    imagen = Image.open(filepath)
    if operacion == 'cambiar_tamaño':
        imagen = imagen.resize((imagen.width // 2, imagen.height // 2))
    elif operacion == 'convertir_a_jpg':
        if imagen.mode != 'RGB':
            imagen = imagen.convert('RGB')
    elif operacion == 'recortar':
        imagen = imagen.crop((50, 50, imagen.width - 50, imagen.height - 50))
    elif operacion == 'rotar':
        imagen = imagen.rotate(90)

    processed_path = os.path.join(PROCESSED_FOLDER, f'processed_{file.filename}')
    imagen.save(processed_path)

    return jsonify({"message": "Imagen procesada", "url": f'/processed/{file.filename}'})

@app.route('/processed/<filename>')
def processed_image(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
