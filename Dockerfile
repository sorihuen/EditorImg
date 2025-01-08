# Usa una imagen base de Python
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema necesarias para Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia el archivo requirements.txt e instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la aplicación al contenedor
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
