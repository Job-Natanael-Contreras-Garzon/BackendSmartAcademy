# Smart Academy Backend

Backend para el sistema de gestión académica con predicción de rendimiento utilizando machine learning y análisis de datos.

## Requisitos

- Python 3.7+
- PostgreSQL
- Librerías: scikit-learn, pandas, numpy, joblib

## Instalación

1. Clona el repositorio
2. Crea un entorno virtual: `python -m venv venv`
3. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
4. Instala las dependencias: `pip install -r requirements.txt`
5. Crea un archivo `.env` con las variables de entorno necesarias
6. Ejecuta las migraciones: `alembic upgrade head`
7. Inicia el servidor: `uvicorn app.main:app --reload`

## Población de datos de prueba

1. Con el entorno virtual activado, ejecuta:
   ```
   python -m app.scripts.populate_db
   ```
2. Este script poblará la base de datos con:
   - Usuarios (profesores y estudiantes)
   - Cursos
   - Calificaciones con tendencias temporales
   - Registros de asistencia
   - Participaciones en clase

## Documentación

La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
## Credenciales del administrador creado:
- Email: admin@smartacademy.com
- Contraseña: admin123
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

### Plan de Implementación Secuencial del Backend SmartAcademy

A continuación, te presento un plan estructurado para implementar los casos de uso del sistema SmartAcademy, organizados en fases secuenciales y distinguiendo entre funcionalidades web y móviles.

## Fase 1: Fundamentos y Autenticación (1-2 semanas)

### Casos de Uso

* CU13: Gestión de autenticación y seguridad (web/mobile)
	+ Descripción: Sistema de login, registro y gestión de tokens JWT.
	+ Endpoints:
		- POST /api/v1/auth/login - Login y obtención de token.
			+ Permisos: Abierto.
		- POST /api/v1/auth/register-admin - Registrar un nuevo usuario administrador.
			+ Permisos: Solo Superusuarios autenticados.
		- GET /api/v1/auth/users/me - Obtener el perfil del usuario actualmente autenticado.
			+ Permisos: Cualquier usuario autenticado.
		- POST /api/v1/auth/change-password - Cambiar la contraseña del usuario actualmente autenticado.
			+ Permisos: Cualquier usuario autenticado.
	+ Funcionalidades móvil: Login con persistencia de sesión, refresh token
	+ Funcionalidades web: Además de lo anterior, gestión de sesiones y cierre de sesión global
	+ Valores de atributos: N/A
* CU1: Gestión de usuarios (web/mobile)
	+ Descripción: CRUD de usuarios con roles definidos.
	+ Endpoints:
		- POST /api/v1/users/ - Crear un nuevo usuario (profesor, estudiante, padre).
			+ Permisos: Solo Superusuarios.
		- GET /api/v1/users/ - Listar todos los usuarios.
			+ Permisos: Solo Superusuarios.
		- GET /api/v1/users/{user_id} - Obtener un usuario específico por su ID.
			+ Permisos: Superusuarios pueden ver cualquier usuario. Usuarios regulares solo pueden ver su propio perfil (si `user_id` coincide con el del token).
		- PUT /api/v1/users/{user_id} - Actualizar un usuario específico por su ID.
			+ Permisos: Superusuarios pueden actualizar cualquier usuario. Usuarios regulares solo pueden actualizar su propio perfil.
		- DELETE /api/v1/users/{user_id} - Eliminar un usuario específico por su ID.
			+ Permisos: Solo Superusuarios.
	+ Funcionalidades móvil: Registro, visualización y edición de perfil básico
	+ Funcionalidades web: Todo lo anterior más gestión completa de usuarios (admin)
	+ Valores de atributos:
		- role: ["student", "teacher", "paterns", "administrator"]
		- gender: ["female", "male", "other"]
* CU2: Gestionar roles y permisos (web/mobile)
	+ Descripción: Sistema para asignar roles y permisos a usuarios.
	+ Endpoints:
		- POST /api/v1/roles/ - Crear un nuevo rol.
			+ Permisos: Solo Administradores.
		- GET /api/v1/roles/ - Listar todos los roles disponibles.
			+ Permisos: Cualquier usuario autenticado.
		- GET /api/v1/roles/{role_id} - Obtener un rol específico por su ID.
			+ Permisos: Cualquier usuario autenticado.
		- PUT /api/v1/roles/{role_id} - Actualizar un rol existente.
			+ Permisos: Solo Administradores.
		- DELETE /api/v1/roles/{role_id} - Eliminar un rol existente.
			+ Permisos: Solo Administradores.
		- POST /api/v1/roles/{role_id}/assign_to_user/{user_id} - Asignar un rol específico a un usuario específico.
			+ Permisos: Solo Administradores.
		- POST /api/v1/roles/{role_id}/remove_from_user/{user_id} - Remover un rol específico de un usuario específico.
			+ Permisos: Solo Administradores.
		- GET /api/v1/users/{user_id}/roles - Obtener los roles asignados a un usuario específico. (Este endpoint reside en el módulo de Usuarios pero es relevante para la gestión de roles).
			+ Permisos: Cualquier usuario autenticado.
	+ Funcionalidades móvil: Visualización de roles propios
	+ Funcionalidades web: Gestión completa de roles y permisos
	+ Valores de atributos: Permisos específicos según rol
## Fase 2: Estructura Académica (2 semanas)
* CU14: Gestión de periodos académicos (web)
	+ Descripción: Configuración de periodos lectivos.
	+ Endpoints:
		- POST /api/v1/periods/ - Crear periodo
		- GET /api/v1/periods/ - Listar periodos
		- PUT /api/v1/periods/{period_id} - Actualizar periodo
	+ Funcionalidades web: Creación y configuración de periodos académicos
	+ Valores de atributos: name - Nombre descriptivo del periodo
* CU3: Gestión de Cursos (web/mobile)
	+ Descripción: CRUD de cursos, asignación de profesores y gestión de estudiantes inscritos.
	+ Endpoints:
		- POST /api/v1/courses/ - Crear un nuevo curso (incluye asignación de profesor).
			+ Permisos: Solo Administradores.
		- GET /api/v1/courses/ - Listar todos los cursos (permite filtros por profesor_id, estudiante_id).
			+ Permisos: Cualquier usuario autenticado.
		- GET /api/v1/courses/{course_id} - Obtener un curso específico por su ID.
			+ Permisos: Cualquier usuario autenticado.
		- PUT /api/v1/courses/{course_id} - Actualizar un curso existente (incluye cambio de profesor).
			+ Permisos: Solo Administradores.
		- DELETE /api/v1/courses/{course_id} - Eliminar un curso.
			+ Permisos: Solo Administradores.
		- POST /api/v1/courses/{course_id}/students - Inscribir estudiantes en un curso.
			+ Permisos: Solo Administradores.
			+ **Estado: Pendiente de Implementación.**
		- DELETE /api/v1/courses/{course_id}/students/{student_id} - Remover un estudiante de un curso.
			+ Permisos: Solo Administradores.
			+ **Estado: Pendiente de Implementación.**
		- GET /api/v1/courses/{course_id}/students - Listar estudiantes inscritos en un curso.
			+ Permisos: Profesores del curso, Administradores.
			+ **Estado: Pendiente de Implementación.**
	+ Funcionalidades móvil: Visualización de cursos asignados/inscritos.
	+ Funcionalidades web: Gestión completa de cursos, profesores y estudiantes en cursos.
	+ Valores de atributos:
		- grade: ["1ro", "2do", "3ro", "4to", "5to", "6to", "kinder", "preescolar"]
		- level: ["initial", "primary", "secondary"]
* CU4: Gestión de asignaturas y criterios de evaluación (web)
	+ Descripción: Configuración de materias y criterios evaluativos.
	+ Endpoints:
		- POST /api/v1/subjects/ - Crear asignatura
		- GET /api/v1/subjects/ - Listar asignaturas
		- POST /api/v1/subjects/{subject_id}/subcriteria - Crear subcriterio
	+ Funcionalidades web: Configuración completa de criterios y ponderaciones
	+ Valores de atributos:
		- Para main_approaches: Ponderaciones (max_weight) configurables
## Fase 3: Gestión Académica (3 semanas)
* CU5: Gestión de notas por periodo y subcriterios (web/mobile)
	+ Descripción: Registro y consulta de calificaciones.
	+ Endpoints:
		- POST /api/v1/grades/ - Registrar nota
		- GET /api/v1/students/{student_id}/grades - Ver notas de estudiante
		- GET /api/v1/subjects/{subject_id}/grades - Ver notas por asignatura
	+ Funcionalidades móvil: Consulta de notas propias (estudiante) o registro rápido (profesor)
	+ Funcionalidades web: Gestión completa, reportes y análisis
	+ Valores de atributos:
		- total_note componentes: ["value_to_be", "value_to_know", "value_to_do", "value_to_decide", "value_to_self-evaluate", "total"]
* CU6: Gestión de asistencias (web/mobile)
	+ Descripción: Registro y consulta de asistencia.
	+ Endpoints:
		- POST /api/v1/attendances/ - Registrar asistencia
		- GET /api/v1/students/{student_id}/attendances - Ver asistencias
	+ Funcionalidades móvil: Registro rápido de asistencia, consulta individual
	+ Funcionalidades web: Gestión masiva, reportes y análisis
	+ Valores de atributos: Presencia booleana (true/false)
* CU8: Gestión de tutor-estudiante (web)
	+ Descripción: Administración de relaciones tutor-estudiante.
	+ Endpoints:
		- POST /api/v1/tutors/ - Asignar tutor
		- GET /api/v1/students/{student_id}/tutors - Ver tutores de estudiante
	+ Funcionalidades web: Gestión completa de relaciones
	+ Valores de atributos:
		- relationship: ["tutor", "partner", "etc"]
## Fase 4: Funcionalidades Avanzadas (3-4 semanas)
* CU9: Gestión de predicción del rendimiento académico (web/mobile)
	+ Descripción: Sistema ML para predicción de rendimiento.
	+ Endpoints:
		- POST /api/v1/predictions/train - Entrenar modelo
		- GET /api/v1/predictions/student/{student_id} - Predecir rendimiento
	+ Funcionalidades móvil: Visualización de predicciones personalizadas
	+ Funcionalidades web: Entrenamiento de modelos, configuración y análisis global
	+ Valores de atributos:
		- Componentes de predicción: ["to be", "to know", "to do", "to decide", "self-assessment"]
* CU10: Gestión de reportes académicos (web/mobile)
	+ Descripción: Generación de reportes académicos.
	+ Endpoints:
		- GET /api/v1/dashboard/stats - Estadísticas generales
		- GET /api/v1/dashboard/student/{student_id} - Reporte individual
	+ Funcionalidades móvil: Reportes personalizados básicos
	+ Funcionalidades web: Reportes completos, exportación a PDF/Excel
	+ Valores de atributos: N/A
* CU15: Gestión de matrículas y pagos (web)
	+ Descripción: Administración de pagos y matrículas.
	+ Endpoints:
		- POST /api/v1/tuitions/ - Registrar matrícula/pago
		- GET /api/v1/students/{student_id}/tuitions - Ver pagos de estudiante
	+ Funcionalidades web: Gestión completa de pagos, reportes y recordatorios
	+ Valores de atributos:
		- status: ["paid", "pending", "overdue"]
		- amount: Valor monetario
		- month: Mes correspondiente
* CU12: Gestión de notificaciones y alertas (web/mobile)
	+ Descripción: Sistema de notificaciones personalizadas.
	+ Endpoints:
		- POST /api/v1/notifications/ - Crear notificación
		- GET /api/v1/users/{user_id}/notifications - Ver notificaciones
		- PUT /api/v1/notifications/{notification_id}/read - Marcar como leída
	+ Funcionalidades móvil: Notificaciones push, alertas personalizadas
	+ Funcionalidades web: Gestión de notificaciones masivas, programación
	+ Valores de atributos: N/A

Consideraciones técnicas
Interfaz web vs. móvil:

## Sistema de Predicción y Análisis

El backend incorpora un avanzado sistema de predicción y análisis del rendimiento académico:

### Características del Sistema ML

- **Extracción de características avanzada**: Análisis de tendencias temporales en calificaciones, asistencia y participación
- **Modelos soportados**: Random Forest, Gradient Boosting, Linear Regression
- **Análisis de riesgo**: Identificación de factores de riesgo específicos para cada estudiante
- **Recomendaciones personalizadas**: Sugerencias automáticas basadas en los patrones detectados
- **Persistencia de modelos**: Almacenamiento de modelos entrenados con versionado temporal
- **Historiales de predicción**: Registro de todas las predicciones para análisis posteriores

### Endpoints de Predicción

- `POST /api/v1/predictions/train`: Entrena un nuevo modelo con los datos disponibles
  - Parámetros: `model_type` (random_forest, gradient_boosting, linear_regression), `advanced` (boolean)
- `GET /api/v1/predictions/student/{student_id}`: Predice el rendimiento de un estudiante
  - Parámetros opcionales: `course_id` (int), `advanced` (boolean)
- `GET /api/v1/predictions/dashboard/stats`: Estadísticas agregadas de predicciones para dashboard
- `GET /api/v1/predictions/at-risk`: Lista de estudiantes en riesgo por nivel
  - Parámetros: `risk_level` (Alto, Medio, Bajo), `limit` (int)

### Script de Análisis

El proyecto incluye un script `app/scripts/analyze_predictions.py` para ejecutar análisis detallados:

```
python -m app.scripts.analyze_predictions
```

Este script:
1. Entrena automáticamente el modelo avanzado
2. Ejecuta predicciones para un conjunto de estudiantes
3. Genera visualizaciones y estadísticas de los resultados
4. Guarda un reporte detallado de las predicciones