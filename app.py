from flask import Flask
from flasgger import Swagger
from src.views.convert import convert_blueprint
from src.views.remove_background import remove_bg_blueprint
from src.views.rotation import rotate_blueprint
from src.views.filter import filtros_blueprint
from src.views.crop_image import crop_blueprint
from src.views.changes_size import resize_blueprint

import os

app = Flask(__name__)
# Configuración básica de Swagger

# Configuración básica de Swagger
swagger = Swagger(app)

# Configuración de la carpeta para guardar imágenes
UPLOAD_FOLDER = './img'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Registrar los Blueprints
app.register_blueprint(convert_blueprint, url_prefix='/convert')
app.register_blueprint(remove_bg_blueprint, url_prefix='/remove-bg')
app.register_blueprint(rotate_blueprint, url_prefix='/rotate')
app.register_blueprint(filtros_blueprint, url_prefix='/filter')
app.register_blueprint(crop_blueprint, url_prefix='/crop')
app.register_blueprint(resize_blueprint, url_prefix='/resize') 


if __name__ == '__main__':
    app.run(debug=True)

