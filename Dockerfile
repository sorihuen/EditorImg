FROM python:3.10-slim

WORKDIR /app

# Instalar las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    llvm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar y instalar las dependencias de Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pre-descargar el modelo U2NET
RUN python -c "from rembg.session_factory import new_session; new_session('u2net')"

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 5000

# Comando para iniciar el servidor Flask con Gunicorn en producción
# Añadido --timeout 300 para dar más tiempo al procesamiento
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--reload", "--timeout", "300", "app:app"]
