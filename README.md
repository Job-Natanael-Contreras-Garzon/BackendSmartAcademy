# Smart Academy Backend

Backend para el sistema de gestión académica con predicción de rendimiento.

## Requisitos

- Python 3.7+
- PostgreSQL

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Crea un archivo [.env](cci:7://file:///c:/Users/contr/Documents/Repositorios%20de%20Git/BackendSmartAcademy/.env:0:0-0:0) con las variables de entorno necesarias
6. Ejecuta las migraciones: `alembic upgrade head`
7. Inicia el servidor: `uvicorn app.main:app --reload`

## Documentación

La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura del proyecto

- `app/` - Código fuente de la aplicación
  - `api/` - Endpoints de la API
  - `core/` - Configuración y utilidades
  - `models/` - Modelos de la base de datos
  - `schemas/` - Esquemas Pydantic
  - `services/` - Lógica de negocio
  - `config/` - Configuración de la base de datos
- `alembic/` - Migraciones de la base de datos
- `tests/` - Pruebas unitarias y de integración