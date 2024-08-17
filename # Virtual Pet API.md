
# Virtual Pet API

## Requisitos previos

- Python 3.7+
- pip
- MongoDB
- OpenSSL (opcional, para HTTPS en desarrollo)

## Configuración del entorno

1. Clonar el repositorio:
   git clone https://github.com/florinato/petApi.git
   cd tu_repositorio

2. Crear y activar entorno virtual:
   python -m venv env
   
   En Windows:
   .\env\Scripts\Activate.ps1
   
   En macOS/Linux:
   source env/bin/activate

3. Instalar dependencias:
   pip install -r requirements.txt

4. Configurar variables de entorno:
   Crear archivo .env en la raíz del proyecto:
   BASE_URL=http://127.0.0.1:8000
   SECRET_KEY=your_secret_key_here
   MONGODB_URI=mongodb://localhost:27017

5. (Opcional) Configurar HTTPS:
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mykey.key -out mycert.crt

6. Ejecutar la aplicación:
   Para HTTP:
   uvicorn main:app --reload
   
   Para HTTPS:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile=./mykey.key --ssl-certfile=./mycert.crt

7. Acceder a la aplicación:
   - Frontend: http://127.0.0.1:8000/
   - Swagger UI: http://127.0.0.1:8000/docs
   - Redoc: http://127.0.0.1:8000/redoc

## Características

- Autenticación JWT
- Gestión de Mascotas (CRUD)
- Frontend Básico
