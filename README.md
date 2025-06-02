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
4. Instala las dependencias: `pip install -r requirements.txt`
5. Crea un archivo [.env](cci:7://file:///c:/Users/contr/Documents/Repositorios%20de%20Git/BackendSmartAcademy/.env:0:0-0:0) con las variables de entorno necesarias
6. Ejecuta las migraciones: `alembic upgrade head`
7. Inicia el servidor: `uvicorn app.main:app --reload`

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
		- POST /api/v1/auth/token - Login y obtención de token
		- GET /api/v1/auth/users/me - Obtener usuario actual
	+ Funcionalidades móvil: Login con persistencia de sesión, refresh token
	+ Funcionalidades web: Además de lo anterior, gestión de sesiones y cierre de sesión global
	+ Valores de atributos: N/A
* CU1: Gestión de usuarios (web/mobile)
	+ Descripción: CRUD de usuarios con roles definidos.
	+ Endpoints:
		- POST /api/v1/users/ - Crear usuario
		- GET /api/v1/users/ - Listar usuarios (admin)
		- GET /api/v1/users/{user_id} - Obtener usuario por ID
		- PUT /api/v1/users/{user_id} - Actualizar usuario
	+ Funcionalidades móvil: Registro, visualización y edición de perfil básico
	+ Funcionalidades web: Todo lo anterior más gestión completa de usuarios (admin)
	+ Valores de atributos:
		- role: ["student", "teacher", "paterns", "administrator"]
		- gender: ["female", "male", "other"]
* CU2: Gestionar roles y permisos (web/mobile)
	+ Descripción: Sistema para asignar roles y permisos a usuarios.
	+ Endpoints:
		- GET /api/v1/roles/ - Listar roles
		- POST /api/v1/roles/ - Crear rol (admin)
		- PUT /api/v1/roles/{role_id} - Actualizar rol
		- POST /api/v1/users/{user_id}/roles - Asignar rol a usuario
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
* CU3: Gestión de grupos escolares (web/mobile)
	+ Descripción: CRUD de grupos escolares y asignación de estudiantes.
	+ Endpoints:
		- POST /api/v1/groups/ - Crear grupo
		- GET /api/v1/groups/ - Listar grupos
		- POST /api/v1/groups/{group_id}/students - Asignar estudiantes
	+ Funcionalidades móvil: Visualización de grupos asignados
	+ Funcionalidades web: Gestión completa de grupos y asignaciones
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