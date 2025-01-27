# Editor de Imagen

Esta es una API de edición de imágenes desarrollada con Flask. Proporciona funcionalidades como rotación de imágenes, eliminación de fondos y aplicación de filtros. 

## Características

- Rotar imágenes en cualquier ángulo.
- Eliminar fondos de imágenes utilizando el modelo U2NET.
- Aplicar filtros como blanco y negro, sepia, borroso, nitidez e invertir colores.
- Documentación interactiva disponible en Swagger.

## Requisitos

- Docker instalado en tu máquina.

## Instalación y Uso

Sigue estos pasos para configurar y ejecutar la aplicación:

### 1. Clona este repositorio
```sh
git clone https://github.com/sorihuen/EditorImg.git

Uso de la API
Endpoints principales
Eliminar fondo de una imagen
URL: POST /remove_bg/
Sube una imagen y elimina su fondo.

Rotar una imagen
URL: POST /rotate/
Sube una imagen y especifica un ángulo para rotarla.

Aplicar filtros a una imagen
URL: POST /filtros/
Sube una imagen y selecciona un filtro (blanco_negro, sepia, etc.).

Para más detalles sobre los parámetros y respuestas, consulta la documentación interactiva.