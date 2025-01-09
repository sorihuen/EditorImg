from flask import Flask
from views import create_routes  # Importar las vistas

app = Flask(__name__)

# Registrar las rutas desde el archivo views.py
create_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
