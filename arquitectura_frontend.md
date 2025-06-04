# Arquitectura Frontend Smart Academy

Este documento define la arquitectura, estructura de navegación y especificaciones para el desarrollo del frontend de Smart Academy, basado en los endpoints y modelos disponibles en el backend.

## Índice

1. [Arquitectura General](#1-arquitectura-general)
2. [Flujo de Desarrollo](#2-flujo-de-desarrollo)
3. [Componentes y Servicios Base](#3-componentes-y-servicios-base)
4. [Módulos y Vistas Principales](#4-módulos-y-vistas-principales)
   - [4.1. Autenticación (CU13)](#41-autenticación-cu13)
   - [4.2. Dashboard (Rol Específico)](#42-dashboard-rol-específico)
   - [4.3. Gestión de Usuarios (Admin - CU1)](#43-gestión-de-usuarios-admin---cu1)
   - [4.4. Gestión de Roles y Permisos (Admin - CU2)](#44-gestión-de-roles-y-permisos-admin---cu2)
   - [4.5. Gestión de Periodos Académicos (Admin - CU14)](#45-gestión-de-periodos-académicos-admin---cu14)
   - [4.6. Gestión de Cursos (Admin, Profesor, Estudiante - CU3)](#46-gestión-de-cursos-admin-profesor-estudiante---cu3)
   - [4.7. Gestión de Asignaturas y Criterios (Admin - CU4)](#47-gestión-de-asignaturas-y-criterios-admin---cu4)
   - [4.8. Gestión de Calificaciones (Profesor, Estudiante - CU5)](#48-gestión-de-calificaciones-profesor-estudiante---cu5)
   - [4.9. Gestión de Asistencia (Profesor, Estudiante - CU6)](#49-gestión-de-asistencia-profesor-estudiante---cu6)
   - [4.10. Gestión de Tutores (Admin, Estudiante - CU8)](#410-gestión-de-tutores-admin-estudiante---cu8)
   - [4.11. Predicciones de Rendimiento IA (Estudiante, Profesor/Admin - CU9)](#411-predicciones-de-rendimiento-ia-estudiante-profesoradmin---cu9)
   - [4.12. Reportes Académicos (CU10)](#412-reportes-académicos-cu10)
   - [4.13. Sistema de Notificaciones (CU11, CU12)](#413-sistema-de-notificaciones-cu11-cu12)
   - [4.14. Configuración de Cuenta](#414-configuración-de-cuenta)
5. [Consideraciones Técnicas](#5-consideraciones-técnicas)

## 1. Arquitectura General

### Tecnologías Recomendadas
- **Framework UI**: React.js o Vue.js
- **Gestión de Estado**: Redux/Vuex o Context API
- **Enrutamiento**: React Router/Vue Router
- **Componentes UI**: Material-UI, Ant Design o Tailwind CSS 
- **Peticiones HTTP**: Axios
- **Notificaciones en tiempo real**: WebSockets (Socket.io)

### Estructura de Carpetas Sugerida (React)
```
src/
├── assets/               # Imágenes, fuentes, archivos estáticos
├── components/           # Componentes UI globales y reutilizables (Button, Input, Card, etc.)
│   ├── common/             # Componentes muy genéricos
│   └── layout/           # Componentes de estructura (Header, Sidebar, Footer)
├── config/               # Configuración de la aplicación (ej. API base URL, constantes)
├── contexts/             # React Contexts para gestión de estado global o temático
├── features/             # Módulos de funcionalidad principal (anteriormente 'modules')
│   ├── auth/
│   │   ├── components/     # Componentes específicos de autenticación (LoginForm, RegisterForm)
│   │   ├── hooks/          # Hooks específicos de autenticación
│   │   ├── services/       # Lógica de llamadas API para autenticación (usa el servicio API general)
│   │   ├── pages/          # Vistas/páginas (LoginPage, RegisterPage, ProfilePage)
│   │   └── state/          # (Opcional) Estado local del feature (ej. con Zustand o Redux Toolkit slice)
│   ├── users/
│   ├── courses/
│   ├── grades/
│   ├── predictions/
│   ├── admin/
│   │   ├── userManagement/
│   │   ├── roleManagement/
│   │   └── periodManagement/
│   └── dashboard/
├── hooks/                # Hooks personalizados globales
├── layouts/              # Layouts principales de la aplicación (AppLayout, AuthLayout, DashboardLayout)
├── lib/                  # Instancias de librerías externas (axiosInstance)
├── pages/                # (Alternativa a features/xxx/pages) Páginas principales si no se usa estructura por feature
├── services/             # Servicios API generales y abstracciones
│   ├── api.service.js      # Configuración base de Axios, interceptores JWT
│   ├── auth.service.js     # Métodos para endpoints de autenticación
│   ├── user.service.js     # Métodos para endpoints de usuarios
│   ├── course.service.js   # Métodos para endpoints de cursos
│   └── ...                 # Otros servicios por entidad/funcionalidad
├── store/                # Configuración de estado global (Redux, Zustand, etc.)
│   ├── slices/           # Si se usa Redux Toolkit
│   └── index.js
├── styles/               # Estilos globales, temas, variables CSS
├── types/                # Definiciones TypeScript globales (interfaces, tipos)
├── utils/                # Funciones de utilidad generales (helpers, formatters)
└── App.tsx               # Componente raíz de la aplicación, configuración de router
```
**Nota:** La estructura de `features/` (o `modules/`) es crucial y debe reflejar la organización del backend y los Casos de Uso.

## 2. Flujo de Desarrollo

### Fase 1: Configuración y Autenticación
1. Configuración del proyecto y dependencias
{{ ... }}

## 4. Módulos y Vistas Principales

Esta sección detalla los módulos y vistas clave de la aplicación, alineados con los Casos de Uso (CU) del backend. Para cada módulo, se describen rutas, componentes, estado, endpoints y flujos.

**Nota sobre Estructura de Datos y Estado:**
Las interfaces TypeScript para el estado y los payloads/respuestas de API deben basarse en los `ejemplosjson.md` y los esquemas Pydantic del backend (visibles en `/docs`).

**Tecnologías Asumidas para Ejemplos:** React, React Router, Axios, y una librería de componentes UI (ej. Material-UI o Ant Design).

### 4.1. Autenticación (CU13)

#### Login
- **Ruta**: `/login`
{{ ... }}
    isLoading: boolean;
    error: string | null;
  }
  ```
- **Endpoints**:
  - `POST /api/v1/auth/login` - Autenticación de usuario.
    - **Payload (según ejemplosjson.md)**: `{ "email": "admin@smartacademy.com", "password": "admin123" }` (el campo `remember_me` no está en el ejemplo JSON, verificar si es necesario o si se maneja de otra forma, ej. duración del token).
    - **Respuesta exitosa (según ejemplosjson.md)**: `{ "access_token", "token_type", "user_id", "email", "full_name", "role", "is_superuser" }`.
    - **Manejo de errores**: Mostrar `LoginErrorMessage` con mensaje de `detail` de la respuesta (ej. "Credenciales incorrectas").
- **Flujo de acciones**:
  1. Usuario ingresa credenciales
  2. Al enviar, mostrar estado de carga en `LoginButton`
  3. Llamar al endpoint de login
  4. Si es exitoso, almacenar token en `AuthService` y redirigir al dashboard según rol
{{ ... }}
      </AuthLayout>
    );
  };
  ```

#### Registro de Administrador (Superusuario)
- **Ruta**: `/admin/register-admin` (Ruta protegida, accesible solo por superusuarios)
- **Componentes**:
  - `AdminRegistrationForm`: Formulario con campos para email, password, full_name, phone, direction, birth_date, gender.
  - `SubmitButton`: Botón de envío con estados de carga.
  - `SuccessMessage`/`ErrorMessage`: Para feedback.
- **Estado**:
  ```typescript
  interface AdminRegistrationState {
    formData: {
      email: string;
      password: string;
      full_name: string;
      phone?: string;
      direction?: string;
      birth_date?: string; // YYYY-MM-DD
      gender?: 'male' | 'female' | 'other';
    };
    isLoading: boolean;
    error: string | null;
    successMessage: string | null;
  }
  ```
- **Endpoints**:
  - `POST /api/v1/auth/register-admin`
    - **Payload**: `{ email, password, full_name, phone, direction, birth_date, gender }`.
    - **Respuesta exitosa**: Datos del nuevo administrador creado.
    - **Manejo de errores**: Mostrar mensajes de `detail` (ej. "El correo electrónico ya está registrado", "No tiene suficientes permisos").
- **Flujo de acciones**:
  1. Superusuario navega a la ruta.
  2. Ingresa datos del nuevo administrador.
  3. Al enviar, se llama a `AuthService.registerAdmin()`.
  4. Mostrar feedback (éxito o error).

#### Perfil del Usuario (Mi Perfil)
- **Ruta**: `/profile` o `/account/me`
- **Componentes**:
  - `UserProfileDisplay`: Muestra la información del usuario actual (full_name, email, role, etc.).
  - `EditProfileButton`: Enlace a una página de edición de perfil (si aplica, ver CU1 PUT /api/v1/users/{user_id}).
  - `ChangePasswordButton`: Enlace a la página de cambio de contraseña.
- **Estado**:
  ```typescript
  interface UserProfileState {
    userData: { // Basado en la respuesta de /api/v1/auth/users/me
      id: number;
      email: string;
      full_name: string;
      phone?: string;
      direction?: string;
      birth_date?: string;
      gender?: string;
      role: string;
      photo?: string | null;
      is_active: boolean;
      is_superuser: boolean;
    } | null;
    isLoading: boolean;
    error: string | null;
  }
  ```
- **Endpoints**:
  - `GET /api/v1/auth/users/me` (Llamado al cargar la página vía `AuthService.getCurrentUser()`)
- **Flujo de acciones**:
  1. Usuario navega a la ruta.
  2. Se obtienen los datos del usuario actual.
  3. Se muestra la información.

#### Cambiar Contraseña
- **Ruta**: `/profile/change-password` o `/account/change-password`
- **Componentes**:
  - `ChangePasswordForm`: Campos para contraseña actual y nueva contraseña (con confirmación).
- **Estado**:
  ```typescript
  interface ChangePasswordState {
    current_password: string;
    new_password: string;
    confirm_password: string;
    isLoading: boolean;
    error: string | null;
    successMessage: string | null;
  }
  ```
- **Endpoints**:
  - `POST /api/v1/auth/change-password`
    - **Payload**: `{ current_password, new_password }`.
    - **Respuesta exitosa**: `{ message: "Contraseña actualizada correctamente" }`.
- **Flujo de acciones**:
  1. Usuario ingresa contraseñas.
  2. Al enviar, se llama a `AuthService.changePassword()`.
  3. Mostrar feedback.

### 4.2. Dashboard (Rol Específico)
- **Ruta**: `/dashboard` (podría redirigir a `/dashboard/student`, `/dashboard/teacher`, `/dashboard/admin` según rol).
- **Descripción**: Página principal después del login. Su contenido varía significativamente según el rol del usuario.
- **Componentes Comunes**:
  - `DashboardLayout`: Layout específico con Sidebar y Header.
  - `WelcomeMessage`: Saludo al usuario.
  - `QuickAccessLinks`: Enlaces a las funcionalidades más usadas por ese rol.
  - `NotificationPanel`: Resumen de notificaciones recientes.
- **Componentes Específicos por Rol**:
  - **Estudiante**: `MyCoursesWidget`, `UpcomingAssignmentsWidget`, `MyPerformanceSnapshotWidget` (con datos de predicción si CU9 está activo).
  - **Profesor**: `MyClassesWidget`, `PendingSubmissionsWidget`, `StudentPerformanceOverviewWidget`.
  - **Administrador**: `SystemStatsWidget` (usuarios, cursos), `AdminToolsWidget` (enlaces a gestión de usuarios, roles, etc.), `ModelTrainingStatusWidget` (si CU9 está activo).
- **Endpoints**: Dependerá de los widgets y datos a mostrar. Puede requerir múltiples llamadas a servicios de cursos, predicciones, usuarios, etc.

### 4.3. Gestión de Usuarios (Admin - CU1)
- **Ruta Base**: `/admin/users`
- **Permisos**: Solo Administradores y Superusuarios.
- **Vistas/Páginas**:
  - **Lista de Usuarios (`/admin/users`)**
    - **Componentes**: `UserTable` (con `DataTable` base), `FilterControls` (filtrar por rol, activo/inactivo), `CreateUserButton`.
    - **Estado**: Lista de usuarios, filtros, paginación.
    - **Endpoint**: `GET /api/v1/users/` (con parámetros de filtro y paginación).
  - **Crear Usuario (`/admin/users/new`)**
    - **Componentes**: `UserForm` (campos: email, password, full_name, phone, direction, birth_date, gender, role).
    - **Estado**: Datos del formulario.
    - **Endpoint**: `POST /api/v1/users/`.
    - **Payload**: `{ email, password, full_name, phone, direction, birth_date, gender, role }` (ver `ejemplosjson.md` para estructura exacta y valores de `gender`, `role`).
  - **Editar Usuario (`/admin/users/:userId/edit`)**
    - **Componentes**: `UserForm` (precargado con datos del usuario, sin campo de contraseña o con manejo especial para cambio de contraseña).
    - **Estado**: Datos del formulario, ID del usuario.
    - **Endpoints**: `GET /api/v1/users/{user_id}` para cargar datos, `PUT /api/v1/users/{user_id}` para guardar.
  - **Ver Detalles del Usuario (`/admin/users/:userId`)**
    - **Componentes**: `UserDetailsDisplay`, `UserRolesList` (ver CU2).
    - **Endpoint**: `GET /api/v1/users/{user_id}`.
- **Servicio**: `UserService`.

### 4.4. Gestión de Roles y Permisos (Admin - CU2)
- **Ruta Base**: `/admin/roles`
- **Permisos**: Solo Administradores.
- **Vistas/Páginas**:
  - **Lista de Roles (`/admin/roles`)**
    - **Componentes**: `RoleTable`, `CreateRoleButton`.
    - **Endpoint**: `GET /api/v1/roles/`.
  - **Crear/Editar Rol (`/admin/roles/new`, `/admin/roles/:roleId/edit`)**
    - **Componentes**: `RoleForm` (nombre del rol, descripción, potencialmente asignación de permisos granulares si el backend lo soporta más allá del nombre del rol).
    - **Endpoints**: `POST /api/v1/roles/`, `PUT /api/v1/roles/{role_id}`.
  - **Asignar Roles a Usuarios**: Esta funcionalidad podría integrarse en la vista de edición de usuario (`/admin/users/:userId/edit`) o en una vista dedicada.
    - **Componentes**: Selector de roles disponibles, lista de roles asignados al usuario.
    - **Endpoints**: `GET /api/v1/users/{user_id}/roles` para ver roles actuales, `POST /api/v1/roles/{role_id}/assign_to_user/{user_id}`, `POST /api/v1/roles/{role_id}/remove_from_user/{user_id}`.
- **Servicio**: `RoleService`, `UserService`.

### 4.5. Gestión de Periodos Académicos (Admin - CU14)
- **Ruta Base**: `/admin/periods`
- **Permisos**: Solo Administradores.
- **Vistas/Páginas**:
  - **Lista de Periodos (`/admin/periods`)**
    - **Componentes**: `PeriodsTable`, `CreatePeriodButton`.
    - **Endpoint**: `GET /api/v1/periods/`.
  - **Crear/Editar Periodo (`/admin/periods/new`, `/admin/periods/:periodId/edit`)**
    - **Componentes**: `PeriodForm` (nombre, fecha de inicio, fecha de fin).
    - **Endpoints**: `POST /api/v1/periods/`, `PUT /api/v1/periods/{period_id}`.
- **Servicio**: `PeriodService`.

### 4.6. Gestión de Cursos (Admin, Profesor, Estudiante - CU3)
- **Ruta Base**: `/courses`
- **Vistas/Páginas (Rol Dependiente)**:
  - **Lista de Cursos (`/courses`)**
    - **Admin/Profesor**: `CourseTable` con opciones de gestión, filtros (por profesor, nivel, grado). `CreateCourseButton` (Admin).
    - **Estudiante**: `EnrolledCoursesList` (tarjetas o lista simple).
    - **Endpoint**: `GET /api/v1/courses/` (con filtros `profesor_id`, `estudiante_id` según rol).
  - **Crear Curso (Admin) (`/admin/courses/new`)**
    - **Componentes**: `CourseForm` (nombre, descripción, profesor asignado, nivel, grado).
    - **Endpoint**: `POST /api/v1/courses/`.
  - **Ver Detalles del Curso (`/courses/:courseId`)**
    - **Admin/Profesor**: `CourseDetailsDisplay`, `StudentListInCourse` (con opción de inscribir/remover para Admin - ver endpoints `.../students`), `CourseAssignmentsList`.
    - **Estudiante**: `CourseDetailsDisplay`, `MyGradesInCourse`, `CourseMaterials`, `AssignmentsList`.
    - **Endpoints**: `GET /api/v1/courses/{course_id}`, `GET /api/v1/courses/{course_id}/students` (Admin/Profesor).
  - **Editar Curso (Admin) (`/admin/courses/:courseId/edit`)**
    - **Componentes**: `CourseForm` precargado.
    - **Endpoint**: `PUT /api/v1/courses/{course_id}`.
  - **Inscribir Estudiantes en Curso (Admin) (`/admin/courses/:courseId/manage-students`)**
    - **Componentes**: Selector de estudiantes, lista de estudiantes inscritos.
    - **Endpoints**: `POST /api/v1/courses/{course_id}/students`, `DELETE /api/v1/courses/{course_id}/students/{student_id}`.
- **Servicio**: `CourseService`, `UserService`.

### 4.7. Gestión de Asignaturas y Criterios (Admin - CU4)
- **Ruta Base**: `/admin/subjects`
- **Permisos**: Solo Administradores.
- **Vistas/Páginas**:
  - **Lista de Asignaturas (`/admin/subjects`)**
    - **Componentes**: `SubjectsTable`, `CreateSubjectButton`.
    - **Estado**: Lista de asignaturas, filtros.
    - **Endpoint**: `GET /api/v1/subjects/`.
  - **Crear/Editar Asignatura (`/admin/subjects/new`, `/admin/subjects/:subjectId/edit`)**
    - **Componentes**: `SubjectForm` (nombre, descripción, ¿asociación a niveles/grados?).
    - **Estado**: Datos del formulario.
    - **Endpoints**: `POST /api/v1/subjects/`, `PUT /api/v1/subjects/{subject_id}`.
  - **Gestionar Subcriterios de Evaluación (`/admin/subjects/:subjectId/subcriteria`)**
    - **Componentes**: `SubcriteriaTable` (para la asignatura seleccionada), `CreateSubcriterionButton`.
    - **Estado**: Lista de subcriterios para la asignatura.
    - **Endpoint (Crear)**: `POST /api/v1/subjects/{subject_id}/subcriteria`.
      - **Payload**: `{ "name": "string", "max_weight": number }`.
    - **Endpoints (Listar, Editar, Eliminar)**: Necesitarían definirse en el backend si no existen (ej. `GET /api/v1/subjects/{subject_id}/subcriteria`, `PUT /api/v1/subcriteria/{subcriterion_id}`, `DELETE /api/v1/subcriteria/{subcriterion_id}`).
- **Servicio**: `SubjectService`.

### 4.8. Gestión de Calificaciones (Profesor, Estudiante - CU5)
- **Ruta Base**: `/grades` (o integrado en vistas de curso/estudiante)
- **Permisos**: Profesor (registrar/editar), Estudiante/Padre (consultar).
- **Vistas/Páginas**:
  - **Registrar/Editar Calificaciones (Profesor) (`/teacher/courses/:courseId/subject/:subjectId/grades`)**
    - **Componentes**: `GradeEntryForm` (selección de estudiante, periodo, subcriterios con campos para `value_to_be`, `value_to_know`, `value_to_do`, `value_to_decide`, `value_to_self-evaluate`). `GradesTable` para visualizar notas existentes del grupo.
    - **Estado**: Datos del formulario, lista de estudiantes del curso, subcriterios de la asignatura.
    - **Endpoints**:
      - `POST /api/v1/grades/` para registrar nuevas calificaciones.
        - **Payload**: `{ student_id, subject_id, period_id, subcriterion_id, value_to_be, value_to_know, value_to_do, value_to_decide, value_to_self_evaluate }` (adaptar según `ejemplosjson.md`).
      - `GET /api/v1/students/{student_id}/grades?subject_id=X&period_id=Y` para ver/editar existentes.
      - `PUT /api/v1/grades/{grade_id}` (si se permite edición individual de registros de nota).
  - **Ver Mis Calificaciones (Estudiante) (`/student/grades` o `/student/courses/:courseId/grades`)**
    - **Componentes**: `GradesDisplayTable` (agrupadas por asignatura/periodo), `GradeCharts`.
    - **Estado**: Lista de calificaciones del estudiante.
    - **Endpoint**: `GET /api/v1/students/{student_id}/grades` (con filtros opcionales por periodo, asignatura).
  - **Ver Calificaciones del Estudiante (Padre)**: Similar al estudiante, pero con selector de hijo si aplica.
- **Servicio**: `GradeService`, `CourseService`, `SubjectService`.

### 4.9. Gestión de Asistencia (Profesor, Estudiante - CU6)
- **Ruta Base**: `/attendance` (o integrado)
- **Permisos**: Profesor (registrar), Estudiante/Padre (consultar).
- **Vistas/Páginas**:
  - **Registrar Asistencia (Profesor) (`/teacher/courses/:courseId/attendance`)**
    - **Componentes**: `AttendanceSheet` (lista de estudiantes del curso, selector de fecha, checkboxes/radios para presente/ausente/tardanza).
    - **Estado**: Fecha seleccionada, lista de estudiantes, estados de asistencia.
    - **Endpoint**: `POST /api/v1/attendances/`.
      - **Payload**: `{ "student_id": number, "course_id": number, "date": "YYYY-MM-DD", "status": "present" | "absent" | "late" }` (puede ser un array de registros).
  - **Ver Mi Asistencia (Estudiante) (`/student/attendance` o `/student/courses/:courseId/attendance`)**
    - **Componentes**: `AttendanceCalendarView`, `AttendanceSummary`.
    - **Estado**: Registros de asistencia del estudiante.
    - **Endpoint**: `GET /api/v1/students/{student_id}/attendances` (con filtros por curso, rango de fechas).
- **Servicio**: `AttendanceService`, `CourseService`.

### 4.10. Gestión de Tutores (Admin, Estudiante - CU8)
- **Ruta Base**: `/tutors`
- **Permisos**: Administrador (asignar), Estudiante/Padre (ver tutores asignados).
- **Vistas/Páginas**:
  - **Asignar Tutor a Estudiante (Admin) (`/admin/students/:studentId/manage-tutors`)**
    - **Componentes**: `TutorAssignmentForm` (selector de usuario tutor, lista de tutores ya asignados al estudiante).
    - **Estado**: ID del estudiante, ID del tutor a asignar.
    - **Endpoints**:
      - `POST /api/v1/tutors/assign` 
        - **Payload**: `{ "student_id": number, "tutor_id": number }`.
      - `GET /api/v1/students/{student_id}/tutors` para listar tutores asignados.
      - `DELETE /api/v1/tutors/remove` (o similar) para desasignar.
        - **Payload**: `{ "student_id": number, "tutor_id": number }`.
  - **Ver Mis Tutores (Estudiante/Padre)**: Podría ser parte del perfil del estudiante.
    - **Componentes**: `TutorListDisplay`.
    - **Endpoint**: `GET /api/v1/students/{student_id}/tutors`.
- **Servicio**: `TutorService`, `UserService`.

### 4.11. Predicciones de Rendimiento IA (Estudiante, Profesor/Admin - CU9)
- **Ruta Base**: `/predictions`
- **Permisos**: Estudiante (ver propia), Profesor (ver de sus estudiantes), Admin (ver todas, entrenar modelo).
- **Vistas/Páginas**:
  - **Ver Mi Predicción (Estudiante) (`/student/my-prediction`)**
    - **Componentes**: `PredictionDisplay` (estado de predicción, factores influyentes si XAI está disponible), `HistoricalPredictionsChart`.
    - **Estado**: Datos de predicción.
    - **Endpoint**: `GET /api/v1/predictions/student/{student_id}`.
  - **Ver Predicciones de Estudiantes (Profesor) (`/teacher/courses/:courseId/predictions`)**
    - **Componentes**: `StudentPredictionTable` (lista de estudiantes del curso con sus predicciones), `RiskIndicator`.
    - **Estado**: Lista de predicciones.
    - **Endpoint**: `GET /api/v1/predictions/course/{course_id}` (o similar, backend debe proveer endpoint para esto).
  - **Panel de Control IA (Admin) (`/admin/ai/predictions`)**
    - **Componentes**: `ModelTrainingButton`, `TrainingStatusDisplay`, `OverallPredictionStats`.
    - **Estado**: Estado del último entrenamiento, estadísticas.
    - **Endpoints**:
      - `POST /api/v1/predictions/train-model`.
      - `GET /api/v1/predictions/status` (o similar para estado del modelo/entrenamiento).
- **Servicio**: `PredictionService`.

### 4.12. Reportes Académicos (CU10)
- **Ruta Base**: `/reports`
- **Permisos**: Administradores, Profesores (según el tipo de reporte).
- **Vistas/Páginas**:
  - **Generador de Reportes (Admin/Profesor) (`/reports/generate`)**
    - **Componentes**: `ReportSelectionForm` (tipo de reporte, filtros: periodo, curso, estudiante, etc.), `GenerateReportButton`.
    - **Estado**: Parámetros del reporte.
    - **Endpoints**: Dependerá de los endpoints específicos que el backend exponga para cada tipo de reporte (ej. `GET /api/v1/reports/academic-summary?student_id=X`, `GET /api/v1/reports/course-performance?course_id=X`).
    - **Respuesta**: Podría ser un JSON para mostrar en frontend o un enlace a un archivo PDF/CSV generado.
- **Servicio**: `ReportService`.

### 4.13. Sistema de Notificaciones (CU11, CU12)
- **Integrado en el Layout Principal** (`Header`, `NotificationCenter`).
- **Permisos**: Todos los usuarios reciben notificaciones relevantes para ellos.
- **Componentes**:
  - `NotificationIcon` (en Header, con contador de no leídas).
  - `NotificationDropdownList` (al hacer clic en el icono).
  - `NotificationPage` (`/notifications` para ver historial completo).
- **Estado Global**: Lista de notificaciones, contador de no leídas.
- **Endpoints**:
  - `GET /api/v1/notifications/` (para obtener notificaciones del usuario).
  - `POST /api/v1/notifications/{notification_id}/mark-as-read`.
- **WebSocket**: Si se usa para tiempo real, `WebSocketService` escuchará eventos y actualizará el estado de notificaciones.
- **Servicio**: `NotificationService`, `WebSocketService`.

### 4.14. Configuración de Cuenta
- **Ruta Base**: `/account` o `/profile` (ya parcialmente cubierto en Autenticación 4.1).
- **Permisos**: Usuario autenticado para su propia cuenta.
- **Vistas/Páginas Adicionales**:
  - **Editar Perfil (`/account/edit-profile`)**
    - **Componentes**: `ProfileForm` (campos: full_name, phone, direction, birth_date, gender, photo).
    - **Estado**: Datos del formulario.
    - **Endpoint**: `PUT /api/v1/users/{user_id}` (usando el ID del usuario actual).
      - **Payload**: Según `ejemplosjson.md` para actualizar usuario.
    - **Componentes**: Switches para activar/desactivar tipos de notificaciones.
    - **Endpoints**: Backend necesitaría endpoints para guardar estas preferencias.
- **Servicio**: `UserService`, `AuthService`.

## 5. Consideraciones Técnicas Adicionales

Esta sección aborda aspectos técnicos transversales importantes para el desarrollo del frontend de Smart Academy.

- **Gestión de Estado Avanzada:**
  - Si bien React Context puede ser suficiente para algunas áreas, para funcionalidades complejas con estado global compartido (ej. datos del usuario autenticado, notificaciones, configuraciones globales de UI), se podría considerar una librería dedicada como Zustand o Redux Toolkit.
  - La elección dependerá de la complejidad creciente de la aplicación y la preferencia del equipo de desarrollo.
  - Se debe priorizar la atomicidad del estado y la optimización de re-renders.

- **Internacionalización (i18n) y Localización (l10n):**
  - Planificar desde el inicio el soporte para múltiples idiomas si es un requerimiento futuro.
  - Utilizar librerías como `i18next` o `react-intl`.
  - Externalizar todas las cadenas de texto a archivos de traducción.
  - Considerar formatos de fecha, números y moneda específicos por localización.

- **Accesibilidad (a11y):**
  - Seguir las directrices WCAG (Web Content Accessibility Guidelines) para asegurar que la aplicación sea usable por personas con diversas capacidades.
  - Uso semántico de HTML, atributos ARIA cuando sea necesario, contraste de color adecuado, navegabilidad por teclado, y compatibilidad con lectores de pantalla.
  - Realizar pruebas de accesibilidad regulares.

- **Pruebas (Testing):**
  - **Pruebas Unitarias**: Para componentes individuales, hooks y funciones de utilidad (ej. con Jest y React Testing Library).
  - **Pruebas de Integración**: Para flujos de usuario que involucran múltiples componentes y servicios (ej. con React Testing Library, simulando interacciones con API mediante mocks de Axios/fetch).
  - **Pruebas End-to-End (E2E)**: Para verificar flujos completos de la aplicación desde la perspectiva del usuario (ej. con Cypress o Playwright). Aunque más costosas de mantener, son valiosas para asegurar la estabilidad de las funcionalidades críticas.
  - Establecer una estrategia de cobertura de pruebas.

- **Optimización del Rendimiento:**
  - **Code Splitting**: Dividir el código en chunks más pequeños que se cargan bajo demanda (React.lazy, Suspense) para reducir el tiempo de carga inicial.
  - **Memoización**: Usar `React.memo`, `useMemo`, `useCallback` para prevenir re-renders innecesarios.
  - **Optimización de Imágenes**: Comprimir imágenes y usar formatos modernos (ej. WebP). Carga diferida (lazy loading) de imágenes.
  - **Virtualización de Listas**: Para listas largas, usar técnicas de virtualización (ej. `react-window` o `react-virtualized`) para renderizar solo los elementos visibles.
  - **Manejo de Caché**: Estrategias de caché para datos de API (ej. con React Query, SWR, o interceptores de Axios).

- **Manejo de Errores y Logging:**
  - Implementar un sistema robusto de manejo de errores en el frontend.
  - Usar Error Boundaries en React para capturar errores en partes de la UI y evitar que toda la aplicación falle.
  - Considerar la integración con servicios de logging y monitoreo de errores en producción (ej. Sentry, LogRocket) para identificar y diagnosticar problemas rápidamente.

- **Seguridad en el Frontend:**
  - Aunque la lógica de negocio principal y la validación crítica residen en el backend, el frontend debe seguir buenas prácticas:
    - Protegerse contra XSS (Cross-Site Scripting) sanitizando entradas y usando correctamente las capacidades de React para renderizar contenido.
    - No almacenar información sensible en `localStorage` si no es estrictamente necesario y está adecuadamente protegida.
    - Asegurar que las comunicaciones con el backend sean siempre sobre HTTPS.
    - Manejo seguro de tokens JWT (ej. almacenarlos en `httpOnly` cookies si el backend lo soporta, o en memoria/`sessionStorage` con precauciones).

- **Convenciones de Código y Linting:**
  - Establecer y seguir convenciones de código consistentes (ej. Airbnb JavaScript Style Guide).
  - Utilizar herramientas de linting (ESLint) y formateo (Prettier) para mantener la calidad y uniformidad del código.
  - Configurar hooks de pre-commit (ej. Husky) para ejecutar linters y formateadores antes de cada commit.


#### Dashboard de Estudiante
- **Ruta**: `/dashboard/student`
- **Componentes**:
  - `StudentStatsSummary`: Resumen de estadísticas académicas
  - `UpcomingAssignmentsCard`: Lista de próximas entregas
  - `GradesOverviewChart`: Gráfico de rendimiento académico
  - `CourseEnrollmentList`: Lista de cursos matriculados
  - `RecentNotifications`: Notificaciones recientes
- **Endpoints**:
  - `GET /api/v1/dashboard/student/stats` - Estadísticas del estudiante
    - **Respuesta**: `{ average_grade, attendance_percentage, pending_assignments, completed_courses }`
  - `GET /api/v1/dashboard/student/upcoming-assignments` - Próximas entregas
  - `GET /api/v1/dashboard/student/grades-overview` - Datos para gráfico de calificaciones
  - `GET /api/v1/dashboard/student/courses` - Cursos matriculados
- **Implementación**:
  ```jsx
  const StudentDashboard = () => {
    const [stats, setStats] = useState(null);
    const [assignments, setAssignments] = useState([]);
    const [gradesData, setGradesData] = useState(null);
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
      const fetchDashboardData = async () => {
        try {
          setLoading(true);
          
          // Realizar todas las peticiones en paralelo
          const [statsRes, assignmentsRes, gradesRes, coursesRes] = await Promise.all([
            api.get('/api/v1/dashboard/student/stats'),
            api.get('/api/v1/dashboard/student/upcoming-assignments'),
            api.get('/api/v1/dashboard/student/grades-overview'),
            api.get('/api/v1/dashboard/student/courses')
          ]);
          
          setStats(statsRes.data);
          setAssignments(assignmentsRes.data);
          setGradesData(gradesRes.data);
          setCourses(coursesRes.data);
        } catch (err) {
          setError('No se pudo cargar la información del dashboard');
          console.error(err);
        } finally {
          setLoading(false);
        }
      };
      
      fetchDashboardData();
    }, []);
    
    if (loading) return <DashboardSkeleton />;
    if (error) return <ErrorAlert message={error} />;
    
    return (
      <DashboardLayout>
        <WelcomeBar username={userProfile.fullName} lastLogin={userProfile.lastLogin} />
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <StudentStatsSummary 
              averageGrade={stats.average_grade}
              attendancePercentage={stats.attendance_percentage}
              pendingAssignments={stats.pending_assignments}
              completedCourses={stats.completed_courses}
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <GradesOverviewChart data={gradesData} />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <UpcomingAssignmentsCard assignments={assignments} />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <RecentNotifications />
          </Grid>
          
          <Grid item xs={12}>
            <CourseEnrollmentList courses={courses} />
          </Grid>
        </Grid>
      </DashboardLayout>
    );
  };
  ```

#### Dashboard de Profesor
- **Ruta**: `/dashboard/teacher`
- **Componentes**:
  - `ClassesOverview`: Resumen de clases asignadas
  - `StudentProgressCard`: Progreso de estudiantes por clase
  - `PendingGradingList`: Lista de entregas pendientes de calificar
  - `UpcomingLessonsTimeline`: Línea de tiempo de próximas clases
  - `AnnouncementCreator`: Creador de anuncios para estudiantes
- **Endpoints**:
  - `GET /api/v1/dashboard/teacher/classes` - Clases asignadas
  - `GET /api/v1/dashboard/teacher/pending-grading` - Entregas pendientes de calificar
  - `GET /api/v1/dashboard/teacher/upcoming-lessons` - Próximas clases
  - `POST /api/v1/announcements` - Crear anuncios
- **Ejemplo de interacción**:
  1. El profesor ve lista de entregas pendientes de calificar en `PendingGradingList`
  2. Al hacer clic en una entrega, navega a `/grading/:assignment_id`
  3. Ingresa calificación y comentarios en `GradingForm`
  4. Al enviar, se llama a `POST /api/v1/grades` con el payload
  5. El sistema actualiza la lista de pendientes y notifica al estudiante

#### Dashboard de Administrador
- **Ruta**: `/dashboard/admin`
- **Componentes**:
  - `SystemOverviewStats`: Estadísticas generales del sistema
  - `RecentActivityLog`: Registro de actividades recientes
  - `UserManagementShortcuts`: Accesos directos a gestión de usuarios
  - `PendingApprovalsCard`: Solicitudes pendientes de aprobación
  - `SystemHealthMonitor`: Monitor de salud del sistema
- **Endpoints**:
  - `GET /api/v1/dashboard/admin/system-stats` - Estadísticas del sistema
  - `GET /api/v1/dashboard/admin/recent-activity` - Actividad reciente
  - `GET /api/v1/dashboard/admin/pending-approvals` - Aprobaciones pendientes
  - `GET /api/v1/dashboard/admin/system-health` - Estado del sistema
- **Implementación**:
- **Endpoints**:
  - `GET /api/v1/dashboard/parent/{parent_id}` - Datos del dashboard
  - `GET /api/v1/tutors/{parent_id}/students` - Estudiantes asociados
  - `GET /api/v1/notifications?limit=5` - Últimas notificaciones

### 4.3 Gestión Académica

Este módulo permite gestionar toda la información académica del sistema, incluyendo cursos, calificaciones y asistencia.

#### Lista de Cursos
- **Ruta**: `/courses`
- **Componentes**:
  - `CourseFilters`: Filtros para búsqueda de cursos
  - `CourseList`: Lista paginada de cursos
  - `CourseCard`: Tarjeta de visualización de curso
  - `EnrollmentButton`: Botón para inscripción a curso
  - `CourseSearchBar`: Barra de búsqueda
- **Endpoints**:
  - `GET /api/v1/courses` - Listado de cursos con filtros
    - **Parámetros**: `{ search, category, status, page, limit }`
    - **Respuesta**: Lista paginada de cursos con metadata
  - `POST /api/v1/enrollments` - Inscribir estudiante a curso
- **Implementación**:
  ```jsx
  const CoursesPage = () => {
    const [courses, setCourses] = useState([]);
    const [filters, setFilters] = useState({
      search: '',
      category: '',
      status: 'active',
      page: 1,
      limit: 10
    });
    const [metadata, setMetadata] = useState({ total: 0, pages: 0 });
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
      fetchCourses();
    }, [filters]);
    
    const fetchCourses = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/v1/courses', { params: filters });
        setCourses(response.data.items);
        setMetadata(response.data.metadata);
      } catch (error) {
        console.error('Error fetching courses:', error);
      } finally {
        setLoading(false);
      }
    };
    
    const handleFilterChange = (name, value) => {
      setFilters(prev => ({
        ...prev,
        [name]: value,
        page: 1 // Reset page when filters change
      }));
    };
    
    const handlePageChange = (page) => {
      setFilters(prev => ({ ...prev, page }));
    };
    
    const handleEnroll = async (courseId) => {
      try {
        await api.post('/api/v1/enrollments', { course_id: courseId });
        toast.success('Inscripción exitosa');
        fetchCourses(); // Refresh course list to update enrollment status
      } catch (error) {
        toast.error('Error al inscribirse: ' + error.response?.data?.detail || 'Inténtelo nuevamente');
      }
    };
    
    return (
      <MainLayout>
        <PageHeader title="Cursos Disponibles" />
        
        <CourseSearchBar 
          value={filters.search}
          onChange={value => handleFilterChange('search', value)}
        />
        
        <CourseFilters 
          filters={filters}
          onChange={handleFilterChange}
        />
        
        {loading ? (
          <CourseListSkeleton />
        ) : (
          <CourseList 
            courses={courses}
            onEnroll={handleEnroll}
          />
        )}
        
        <Pagination 
          current={filters.page}
          total={metadata.pages}
          onChange={handlePageChange}
        />
      </MainLayout>
    );
  };
  ```

#### Detalle de Curso
- **Ruta**: `/courses/:id`
- **Componentes**:
  - `CourseHeader`: Cabecera con información principal
  - `CourseSyllabus`: Programa del curso
  - `CourseResources`: Recursos disponibles
  - `StudentList`: Lista de estudiantes inscritos (solo docentes)
  - `GradeEntryForm`: Formulario para ingreso de calificaciones (solo docentes)
- **Endpoints**:
  - `GET /api/v1/courses/:id` - Detalle del curso
  - `GET /api/v1/courses/:id/students` - Estudiantes inscritos
  - `GET /api/v1/courses/:id/resources` - Materiales del curso
  - `POST /api/v1/grades` - Registrar calificaciones
- **Flujos de usuario**:
  - **Estudiante**: Ver información, descargar recursos, revisar calificaciones
  - **Profesor**: Además puede gestionar contenido y registrar calificaciones
  - **Admin**: Puede editar configuración del curso y gestionar inscripciones

#### Calificaciones

Este módulo gestiona la interacción entre los diferentes actores de la institución educativa.

#### Directorio de Miembros
- **Ruta**: `/community/directory`
- **Componentes**:
  - `DirectoryFilters`: Filtros por rol, departamento y estado
  - `MembersList`: Lista de miembros con búsqueda y paginación
  - `MemberCard`: Tarjeta con información de contacto y acciones
  - `ProfileViewer`: Visor de perfil completo
  - `ContactButtons`: Botones para comunicación rápida
- **Endpoints**:
  - `GET /api/v1/users` - Listado de usuarios con filtros
    - **Parámetros**: `{ search, role, department, status, page, limit }`
  - `GET /api/v1/users/:id` - Detalles de perfil de usuario
- **Implementación**:
  ```jsx
  const CommunityDirectory = () => {
    const [members, setMembers] = useState([]);
    const [selectedMember, setSelectedMember] = useState(null);
    const [filters, setFilters] = useState({
      search: '',
      role: '',
      department: '',
      status: 'active',
      page: 1,
      limit: 20
    });
    const [metadata, setMetadata] = useState({ total: 0, pages: 0 });
    
    useEffect(() => {
      fetchMembers();
    }, [filters]);
    
    const fetchMembers = async () => {
      try {
        const response = await api.get('/api/v1/users', { params: filters });
        setMembers(response.data.items);
        setMetadata(response.data.metadata);
      } catch (error) {
        console.error('Error fetching community members:', error);
      }
    };
    
    const handleFilterChange = (name, value) => {
      setFilters(prev => ({
        ...prev,
        [name]: value,
        page: 1 // Reset page when filters change
      }));
    };
    
    const handleViewProfile = async (userId) => {
      try {
        const response = await api.get(`/api/v1/users/${userId}`);
        setSelectedMember(response.data);
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };
    
    const handleInitiateContact = (method, userData) => {
      switch (method) {
        case 'email':
          window.location.href = `mailto:${userData.email}`;
          break;
        case 'message':
          // Abrir chat interno
          break;
        case 'call':
          window.location.href = `tel:${userData.phone}`;
          break;
      }
    };
    
    return (
      <MainLayout>
        <PageHeader title="Directorio de la Comunidad" />
        
        <DirectoryFilters 
          filters={filters}
          onChange={handleFilterChange}
        />
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={selectedMember ? 8 : 12}>
            <MembersList 
              members={members}
              onViewProfile={handleViewProfile}
              onInitiateContact={handleInitiateContact}
            />
            
            <Pagination 
              current={filters.page}
              total={metadata.pages}
              onChange={page => setFilters({...filters, page})}
            />
          </Grid>
          
          {selectedMember && (
            <Grid item xs={12} md={4}>
              <ProfileViewer 
                userData={selectedMember}
                onClose={() => setSelectedMember(null)}
                onInitiateContact={handleInitiateContact}
              />
            </Grid>
          )}
        </Grid>
      </MainLayout>
    );
  };
  ```

#### Mensajería Interna
- **Ruta**: `/messages`
- **Componentes**:
  - `ConversationList`: Lista de conversaciones activas
  - `MessageThread`: Hilo de mensajes con usuario
  - `MessageComposer`: Compositor de mensajes con adjuntos
  - `ContactSelector`: Selector de contactos para nuevos mensajes
  - `MessageNotifier`: Notificador de mensajes nuevos
- **Endpoints**:
  - `GET /api/v1/messages` - Listar conversaciones
  - `GET /api/v1/messages/:conversation_id` - Ver mensajes de conversación
  - `POST /api/v1/messages` - Enviar nuevo mensaje
  - `PUT /api/v1/messages/:id/read` - Marcar mensaje como leído
- **Flujo de uso**:
  1. Usuario ve lista de conversaciones con últimos mensajes
  2. Al seleccionar conversación, cargar historial completo
  3. Al escribir, indicador de "escribiendo" para receptor
  4. Enviar mensajes con texto y adjuntos permitidos
  5. Notificaciones push cuando se reciben mensajes nuevos

#### Foros y Discusiones
- **Ruta**: `/forums`
- **Componentes**:
  - `ForumCategories`: Listado de categorías disponibles
  - `TopicList`: Lista de temas en categoría
  - `DiscussionThread`: Hilo de discusión completo
  - `ReplyComposer`: Editor para responder con formato enriquecido
  - `TopicCreator`: Creador de nuevos temas
- **Endpoints**:
  - `GET /api/v1/forums` - Listar categorías de foros
  - `GET /api/v1/forums/:id/topics` - Listar temas en categoría
  - `GET /api/v1/topics/:id` - Ver hilo de discusión completo
  - `POST /api/v1/topics` - Crear nuevo tema
  - `POST /api/v1/topics/:id/replies` - Responder a tema
- **Implementación de Editor de Respuestas**:
  ```jsx
  const ReplyComposer = ({ topicId, onReplyAdded }) => {
    const [content, setContent] = useState('');
    const [attachments, setAttachments] = useState([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(null);
    const editorRef = useRef(null);
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!content.trim()) return;
      
      setIsSubmitting(true);
      setError(null);
      
      try {
        // Preparar formData para adjuntos
        const formData = new FormData();
        formData.append('content', content);
        formData.append('topic_id', topicId);
        
        attachments.forEach(file => {
          formData.append('attachments', file);
        });
        
        const response = await api.post(
          `/api/v1/topics/${topicId}/replies`, 
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        );
        
        // Limpiar campos
        setContent('');
        setAttachments([]);
        editorRef.current?.clear?.();
        
        // Notificar al componente padre
        onReplyAdded(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Error al publicar respuesta');
      } finally {
        setIsSubmitting(false);
      }
    };
    
    const handleFileUpload = (e) => {
      const files = Array.from(e.target.files);
      setAttachments(prev => [...prev, ...files]);
    };
    
    const removeAttachment = (index) => {
      setAttachments(prev => prev.filter((_, i) => i !== index));
    };
    
    return (
      <Paper className="reply-composer" elevation={2}>
        <form onSubmit={handleSubmit}>
          {error && <Alert severity="error">{error}</Alert>}
          
          <RichTextEditor
            ref={editorRef}
            value={content}
            onChange={setContent}
            placeholder="Escribe tu respuesta aquí..."
          />
          
          <AttachmentList
            files={attachments}
            onRemove={removeAttachment}
          />
          
          <div className="composer-actions">
            <input
              type="file"
              id="attachment-input"
              multiple
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            
            <label htmlFor="attachment-input">
              <Button
                component="span"
                startIcon={<AttachFileIcon />}
                size="small"
              >
                Adjuntar
              </Button>
            </label>
            
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={isSubmitting || !content.trim()}
              endIcon={isSubmitting ? <CircularProgress size={20} /> : null}
            >
              Responder
            </Button>
          </div>
        </form>
      </Paper>
    );
  };
  ```

#### Directorio de Estudiantes
- **Ruta**: `/students`
- **Endpoints**:
  - `GET /api/v1/students` - Lista de estudiantes con paginación
  - `GET /api/v1/groups` - Grupos (para filtrado)

#### Perfil de Estudiante
- **Ruta**: `/students/{student_id}`
- **Endpoints**:
  - `GET /api/v1/students/{student_id}` - Datos del estudiante
  - `GET /api/v1/grades/student/{student_id}` - Calificaciones
  - `GET /api/v1/attendance/student/{student_id}` - Asistencias
  - `GET /api/v1/tutors/student/{student_id}` - Tutores asociados

#### Directorio de Profesores
- **Ruta**: `/teachers`
- **Endpoints**:
  - `GET /api/v1/teachers` - Lista de profesores
  - `GET /api/v1/subjects` - Materias (para filtrado)

#### Perfil de Profesor
- **Ruta**: `/teachers/{teacher_id}`
- **Endpoints**:
  - `GET /api/v1/teachers/{teacher_id}` - Datos del profesor
  - `GET /api/v1/courses/teacher/{teacher_id}` - Cursos asignados

#### Gestión de Tutores
- **Ruta**: `/tutors`
- **Endpoints**:
  - `GET /api/v1/tutors` - Lista de tutores
  - `GET /api/v1/tutors/{tutor_id}/students` - Estudiantes asociados
  - `POST /api/v1/tutors/associate` - Asociar tutor con estudiante

### 4.5 Administración

#### Gestión de Matrículas
- **Ruta**: `/tuitions`
- **Endpoints**:
  - `GET /api/v1/tuitions` - Lista de matrículas
  - `POST /api/v1/tuitions` - Crear matrícula
  - `GET /api/v1/students` - Estudiantes disponibles

#### Pagos y Facturación
- **Ruta**: `/tuitions/payments`
- **Endpoints**:
  - `GET /api/v1/tuitions/{tuition_id}/payments` - Pagos de matrícula
  - `POST /api/v1/tuitions/{tuition_id}/payments` - Registrar pago

#### Gestión de Grupos
- **Ruta**: `/groups`
- **Endpoints**:
  - `GET /api/v1/groups` - Lista de grupos
  - `POST /api/v1/groups` - Crear grupo
  - `PUT /api/v1/groups/{group_id}` - Actualizar grupo

#### Asignación de Estudiantes a Grupos
- **Ruta**: `/groups/{group_id}/students`
- **Endpoints**:
  - `GET /api/v1/groups/{group_id}/students` - Estudiantes del grupo
  - `POST /api/v1/groups/{group_id}/students` - Asignar estudiantes
  - `GET /api/v1/students?not_in_group={group_id}` - Estudiantes disponibles

#### Gestión de Usuarios
- **Ruta**: `/users`
- **Endpoints**:
  - `GET /api/v1/users` - Lista de usuarios
  - `POST /api/v1/users` - Crear usuario
  - `PUT /api/v1/users/{user_id}` - Actualizar usuario
  - `GET /api/v1/roles` - Roles disponibles

### 4.6 Sistema de Notificaciones

Este módulo permite la gestión centralizada de notificaciones entre todos los usuarios del sistema.

#### Centro de Notificaciones
- **Ruta**: `/notifications`
- **Componentes**:
  - `NotificationCenter`: Componente central que muestra todas las notificaciones
  - `NotificationItem`: Elemento individual de notificación con acciones
  - `NotificationFilters`: Filtros por tipo, leído/no leído, fecha
  - `NotificationCounter`: Contador de notificaciones no leídas en header
  - `NotificationPreferences`: Panel de preferencias de notificación
- **Endpoints**:
  - `GET /api/v1/notifications` - Listar notificaciones
    - **Parámetros**: `{ read, type, priority, from_date, to_date, page, limit }`
  - `PUT /api/v1/notifications/{notification_id}/read` - Marcar como leída
  - `DELETE /api/v1/notifications/{notification_id}` - Eliminar notificación
- **Implementación**:
  ```jsx
  const NotificationCenter = () => {
    const [notifications, setNotifications] = useState([]);
    const [filters, setFilters] = useState({
      read: null, // null = todas, true = leídas, false = no leídas
      type: '',
      priority: '',
      page: 1,
      limit: 20
    });
    const [metadata, setMetadata] = useState({ total: 0, unread: 0, pages: 0 });
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
      fetchNotifications();
    }, [filters]);
    
    const fetchNotifications = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/v1/notifications', { params: filters });
        setNotifications(response.data.items);
        setMetadata(response.data.metadata);
      } catch (error) {
        console.error('Error fetching notifications:', error);
      } finally {
        setLoading(false);
      }
    };
    
    const handleFilterChange = (name, value) => {
      setFilters(prev => ({
        ...prev,
        [name]: value,
        page: 1 // Resetear página al cambiar filtros
      }));
    };
    
    const handleMarkAsRead = async (notificationId) => {
      try {
        await api.put(`/api/v1/notifications/${notificationId}/read`);
        // Actualizar localmente para evitar refetch
        setNotifications(prev => prev.map(notification => {
          if (notification.id === notificationId) {
            return { ...notification, read: true };
          }
          return notification;
        }));
        // Actualizar contador
        setMetadata(prev => ({ ...prev, unread: Math.max(0, prev.unread - 1) }));
      } catch (error) {
        console.error('Error marking notification as read:', error);
      }
    };
    
    const handleMarkAllAsRead = async () => {
      try {
        await api.put('/api/v1/notifications/read-all');
        // Actualizar localmente
        setNotifications(prev => prev.map(notification => ({ ...notification, read: true })));
        setMetadata(prev => ({ ...prev, unread: 0 }));
      } catch (error) {
        console.error('Error marking all notifications as read:', error);
      }
    };
    
    const handleDeleteNotification = async (notificationId) => {
      try {
        await api.delete(`/api/v1/notifications/${notificationId}`);
        // Eliminar localmente
        setNotifications(prev => prev.filter(notification => notification.id !== notificationId));
        // Actualizar contador si era no leída
        const wasUnread = notifications.find(n => n.id === notificationId)?.read === false;
        if (wasUnread) {
          setMetadata(prev => ({ ...prev, unread: Math.max(0, prev.unread - 1), total: prev.total - 1 }));
        } else {
          setMetadata(prev => ({ ...prev, total: prev.total - 1 }));
        }
      } catch (error) {
        console.error('Error deleting notification:', error);
      }
    };
    
    return (
      <MainLayout>
        <PageHeader 
          title="Centro de Notificaciones" 
          actions={[
            <Button 
              onClick={handleMarkAllAsRead}
              disabled={metadata.unread === 0}
              startIcon={<DoneAllIcon />}
            >
              Marcar todas como leídas
            </Button>
          ]}
        />
        
        <NotificationFilters 
          filters={filters}
          onChange={handleFilterChange}
        />
        
        <Paper elevation={2}>
          {loading ? (
            <NotificationSkeleton count={5} />
          ) : notifications.length > 0 ? (
            <List>
              {notifications.map(notification => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={handleMarkAsRead}
                  onDelete={handleDeleteNotification}
                />
              ))}
              
              <Pagination 
                current={filters.page}
                total={metadata.pages}
                onChange={page => setFilters({...filters, page})}
              />
            </List>
          ) : (
            <EmptyState 
              icon={<NotificationsOffIcon />}
              message="No hay notificaciones"
              description="No tienes notificaciones que coincidan con los filtros seleccionados."
            />
          )}
        </Paper>
      </MainLayout>
    );
  };
  ```

#### Creación de Notificaciones
- **Ruta**: `/notifications/create`
- **Componentes**:
  - `NotificationCreationForm`: Formulario para crear notificaciones
  - `RecipientSelector`: Selector de destinatarios (individual o grupos)
  - `NotificationTypeSelector`: Selector de tipo de notificación
  - `NotificationPrioritySelector`: Selector de prioridad
  - `MessageEditor`: Editor de contenido con formato enriquecido
- **Endpoints**:
  - `POST /api/v1/notifications` - Crear notificación individual
  - `POST /api/v1/notifications/bulk` - Crear notificaciones masivas
  - `GET /api/v1/users` - Usuarios disponibles (para destinatarios)
  - `GET /api/v1/groups` - Grupos disponibles (para envíos masivos)
- **Implementación**:
  ```jsx
  const NotificationCreationPage = () => {
    const [formData, setFormData] = useState({
      title: '',
      content: '',
      type: 'ANNOUNCEMENT',
      priority: 'NORMAL',
      recipients: [],
      selectedGroups: [],
      scheduleDate: null,
      attachments: []
    });
    const [recipientMode, setRecipientMode] = useState('individual'); // 'individual' o 'group'
    const [users, setUsers] = useState([]);
    const [groups, setGroups] = useState([]);
    const [loading, setLoading] = useState(false);
    const [sending, setSending] = useState(false);
    const [success, setSuccess] = useState(false);
    const navigate = useNavigate();
    
    useEffect(() => {
      // Cargar usuarios y grupos disponibles
      const fetchData = async () => {
        setLoading(true);
        try {
          const [usersResponse, groupsResponse] = await Promise.all([
            api.get('/api/v1/users'),
            api.get('/api/v1/groups')
          ]);
          setUsers(usersResponse.data.items || []);
          setGroups(groupsResponse.data || []);
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          setLoading(false);
        }
      };
      
      fetchData();
    }, []);
    
    const handleInputChange = (name, value) => {
      setFormData(prev => ({ ...prev, [name]: value }));
    };
    
    const handleRecipientModeChange = (mode) => {
      setRecipientMode(mode);
      // Limpiar selecciones previas
      setFormData(prev => ({
        ...prev,
        recipients: [],
        selectedGroups: []
      }));
    };
    
    const handleSelectRecipients = (selectedIds) => {
      setFormData(prev => ({
        ...prev,
        recipients: selectedIds
      }));
    };
    
    const handleSelectGroups = (selectedIds) => {
      setFormData(prev => ({
        ...prev,
        selectedGroups: selectedIds
      }));
    };
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!formData.title || !formData.content || 
          (recipientMode === 'individual' && formData.recipients.length === 0) ||
          (recipientMode === 'group' && formData.selectedGroups.length === 0)) {
        return; // Validación básica
      }
      
      setSending(true);
      try {
        // Determinar endpoint basado en modo de envío
        if (recipientMode === 'individual') {
          await api.post('/api/v1/notifications', {
            title: formData.title,
            content: formData.content,
            type: formData.type,
            priority: formData.priority,
            recipient_ids: formData.recipients,
            schedule_date: formData.scheduleDate
          });
        } else {
          await api.post('/api/v1/notifications/bulk', {
            title: formData.title,
            content: formData.content,
            type: formData.type,
            priority: formData.priority,
            group_ids: formData.selectedGroups,
            schedule_date: formData.scheduleDate
          });
        }
        
        setSuccess(true);
        
        // Redireccionar después de un breve delay
        setTimeout(() => {
          navigate('/notifications');
        }, 2000);
      } catch (error) {
        console.error('Error creating notification:', error);
      } finally {
        setSending(false);
      }
    };
    
    if (loading) {
      return <LoadingIndicator message="Cargando datos..." />;
    }
    
    if (success) {
      return (
        <SuccessMessage 
          message="Notificación creada exitosamente" 
          description="Redirigiendo al centro de notificaciones..."
        />
      );
    }
    
    return (
      <MainLayout>
        <PageHeader title="Crear Notificación" />
        
        <Paper elevation={2} sx={{ p: 3 }}>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <FormControl component="fieldset">
                  <FormLabel component="legend">Modo de envío</FormLabel>
                  <RadioGroup 
                    row 
                    value={recipientMode} 
                    onChange={(e) => handleRecipientModeChange(e.target.value)}
                  >
                    <FormControlLabel value="individual" control={<Radio />} label="Destinatarios individuales" />
                    <FormControlLabel value="group" control={<Radio />} label="Envío por grupos" />
                  </RadioGroup>
                </FormControl>
              </Grid>
              
              {/* Selector de destinatarios basado en modo */}
              <Grid item xs={12}>
                {recipientMode === 'individual' ? (
                  <RecipientSelector 
                    users={users} 
                    selectedIds={formData.recipients}
                    onChange={handleSelectRecipients}
                  />
                ) : (
                  <GroupSelector 
                    groups={groups} 
                    selectedIds={formData.selectedGroups}
                    onChange={handleSelectGroups}
                  />
                )}
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  label="Título"
                  fullWidth
                  required
                  value={formData.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <NotificationTypeSelector 
                  value={formData.type}
                  onChange={(value) => handleInputChange('type', value)}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <NotificationPrioritySelector 
                  value={formData.priority}
                  onChange={(value) => handleInputChange('priority', value)}
                />
              </Grid>
              
              <Grid item xs={12}>
                <MessageEditor 
                  value={formData.content}
                  onChange={(value) => handleInputChange('content', value)}
                  placeholder="Escribe el contenido de la notificación aquí..."
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <DateTimePicker 
                  label="Programar envío (opcional)"
                  value={formData.scheduleDate}
                  onChange={(date) => handleInputChange('scheduleDate', date)}
                  minDateTime={new Date()}
                  clearable
                />
              </Grid>
              
              <Grid item xs={12} sx={{ mt: 3 }}>
                <Box display="flex" justifyContent="flex-end">
                  <Button 
                    variant="outlined" 
                    sx={{ mr: 2 }}
                    onClick={() => navigate('/notifications')}
                  >
                    Cancelar
                  </Button>
                  <Button 
                    type="submit" 
                    variant="contained" 
                    color="primary"
                    disabled={sending}
                    startIcon={sending ? <CircularProgress size={20} /> : <SendIcon />}
                  >
                    {sending ? 'Enviando...' : 'Enviar Notificación'}
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </form>
        </Paper>
      </MainLayout>
    );
  };
  ```

#### Preferencias de Notificaciones
- **Ruta**: `/notifications/preferences`
- **Componentes**:
  - `NotificationPreferencesForm`: Formulario para configurar preferencias
  - `NotificationChannelSettings`: Configuración por canal (email, push, in-app)
  - `NotificationTypeToggle`: Activar/desactivar por tipo de notificación
  - `DevicesList`: Lista de dispositivos registrados
  - `TimeRangeSelector`: Selector de horario permitido para notificaciones
- **Endpoints**:
  - `GET /api/v1/devices` - Dispositivos registrados
  - `GET /api/v1/devices/preferences` - Preferencias actuales
  - `PUT /api/v1/devices/preferences` - Actualizar preferencias
  - `DELETE /api/v1/devices/:id` - Eliminar dispositivo registrado
- **Implementación**:
  ```jsx
  const NotificationPreferencesPage = () => {
    const [preferences, setPreferences] = useState({
      emailEnabled: true,
      pushEnabled: true,
      inAppEnabled: true,
      notificationTypes: {
        ACADEMIC: { enabled: true, channels: ['email', 'push', 'inApp'] },
        ANNOUNCEMENT: { enabled: true, channels: ['email', 'push', 'inApp'] },
        ALERT: { enabled: true, channels: ['email', 'push', 'inApp'] },
        EVENT: { enabled: true, channels: ['email', 'push', 'inApp'] },
        MESSAGE: { enabled: true, channels: ['email', 'push', 'inApp'] }
      },
      quietHours: {
        enabled: false,
        start: '22:00',
        end: '08:00'
      }
    });
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [success, setSuccess] = useState(false);
    
    useEffect(() => {
      const fetchPreferences = async () => {
        setLoading(true);
        try {
          const [prefsResponse, devicesResponse] = await Promise.all([
            api.get('/api/v1/devices/preferences'),
            api.get('/api/v1/devices')
          ]);
          
          if (prefsResponse.data) {
            setPreferences(prefsResponse.data);
          }
          
          setDevices(devicesResponse.data || []);
        } catch (error) {
          console.error('Error fetching notification preferences:', error);
        } finally {
          setLoading(false);
        }
      };
      
      fetchPreferences();
    }, []);
    
    const handleToggleChannel = (channel, enabled) => {
      setPreferences(prev => ({
        ...prev,
        [`${channel}Enabled`]: enabled
      }));
      
      // Si se desactiva un canal, quitar ese canal de todos los tipos
      if (!enabled) {
        setPreferences(prev => {
          const updatedTypes = {};
          Object.keys(prev.notificationTypes).forEach(type => {
            updatedTypes[type] = {
              ...prev.notificationTypes[type],
              channels: prev.notificationTypes[type].channels.filter(c => c !== channel)
            };
          });
          return {
            ...prev,
            notificationTypes: updatedTypes
          };
        });
      }
    };
    
    const handleToggleNotificationType = (type, enabled) => {
      setPreferences(prev => ({
        ...prev,
        notificationTypes: {
          ...prev.notificationTypes,
          [type]: {
            ...prev.notificationTypes[type],
            enabled
          }
        }
      }));
    };
    
    const handleToggleTypeChannel = (type, channel, enabled) => {
      setPreferences(prev => {
        const currentChannels = prev.notificationTypes[type].channels;
        let updatedChannels;
        
        if (enabled && !currentChannels.includes(channel)) {
          updatedChannels = [...currentChannels, channel];
        } else if (!enabled && currentChannels.includes(channel)) {
          updatedChannels = currentChannels.filter(c => c !== channel);
        } else {
          updatedChannels = currentChannels;
        }
        
        return {
          ...prev,
          notificationTypes: {
            ...prev.notificationTypes,
            [type]: {
              ...prev.notificationTypes[type],
              channels: updatedChannels
            }
          }
        };
      });
    };
    
    const handleToggleQuietHours = (enabled) => {
      setPreferences(prev => ({
        ...prev,
        quietHours: {
          ...prev.quietHours,
          enabled
        }
      }));
    };
    
    const handleQuietHoursChange = (field, value) => {
      setPreferences(prev => ({
        ...prev,
        quietHours: {
          ...prev.quietHours,
          [field]: value
        }
      }));
    };
    
    const handleRemoveDevice = async (deviceId) => {
      try {
        await api.delete(`/api/v1/devices/${deviceId}`);
        setDevices(prev => prev.filter(device => device.id !== deviceId));
      } catch (error) {
        console.error('Error removing device:', error);
      }
    };
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      setSaving(true);
      
      try {
        await api.put('/api/v1/devices/preferences', preferences);
        setSuccess(true);
        
        // Resetear mensaje de éxito después de un tiempo
        setTimeout(() => {
          setSuccess(false);
        }, 3000);
      } catch (error) {
        console.error('Error saving preferences:', error);
      } finally {
        setSaving(false);
      }
    };
    
    if (loading) {
      return <LoadingIndicator message="Cargando preferencias..." />;
    }
    
    return (
      <MainLayout>
        <PageHeader title="Preferencias de Notificaciones" />
        
        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            Preferencias guardadas exitosamente
          </Alert>
        )}
        
        <Paper elevation={2} sx={{ p: 3 }}>
          <form onSubmit={handleSubmit}>
            <Typography variant="h6" gutterBottom>Canales de Notificación</Typography>
            
            <Grid container spacing={2} sx={{ mb: 4 }}>
              <Grid item xs={12} md={4}>
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.emailEnabled} 
                      onChange={(e) => handleToggleChannel('email', e.target.checked)}
                    />
                  }
                  label="Correo Electrónico"
                />
              </Grid>
              
              <Grid item xs={12} md={4}>
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.pushEnabled} 
                      onChange={(e) => handleToggleChannel('push', e.target.checked)}
                    />
                  }
                  label="Notificaciones Push"
                />
              </Grid>
              
              <Grid item xs={12} md={4}>
                <FormControlLabel
                  control={
                    <Switch 
                      checked={preferences.inAppEnabled} 
                      onChange={(e) => handleToggleChannel('inApp', e.target.checked)}
                    />
                  }
                  label="Notificaciones en la Aplicación"
                />
              </Grid>
            </Grid>
            
            <Divider sx={{ my: 3 }} />
            
            <Typography variant="h6" gutterBottom>Configuración por Tipo de Notificación</Typography>
            
            {Object.entries(preferences.notificationTypes).map(([type, settings]) => (
              <Box key={type} sx={{ mb: 3 }}>
                <Typography variant="subtitle1">
                  {getNotificationTypeLabel(type)}
                  <Switch 
                    size="small"
                    checked={settings.enabled}
                    onChange={(e) => handleToggleNotificationType(type, e.target.checked)}
                  />
                </Typography>
                
                {settings.enabled && (
                  <Box sx={{ pl: 3, mt: 1 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Canales activos para este tipo:
                    </Typography>
                    
                    <FormGroup row>
                      <FormControlLabel
                        disabled={!preferences.emailEnabled}
                        control={
                          <Checkbox 
                            checked={settings.channels.includes('email') && preferences.emailEnabled}
                            onChange={(e) => handleToggleTypeChannel(type, 'email', e.target.checked)}
                            size="small"
                          />
                        }
                        label="Email"
                      />
                      
                      <FormControlLabel
                        disabled={!preferences.pushEnabled}
                        control={
                          <Checkbox 
                            checked={settings.channels.includes('push') && preferences.pushEnabled}
                            onChange={(e) => handleToggleTypeChannel(type, 'push', e.target.checked)}
                            size="small"
                          />
                        }
                        label="Push"
                      />
                      
                      <FormControlLabel
                        disabled={!preferences.inAppEnabled}
                        control={
                          <Checkbox 
                            checked={settings.channels.includes('inApp') && preferences.inAppEnabled}
                            onChange={(e) => handleToggleTypeChannel(type, 'inApp', e.target.checked)}
                            size="small"
                          />
                        }
                        label="En-App"
                      />
                    </FormGroup>
                  </Box>
                )}
              </Box>
            ))}
            
            <Divider sx={{ my: 3 }} />
            
            <Typography variant="h6" gutterBottom>Horarios Silenciosos</Typography>
            
            <Box sx={{ mb: 3 }}>
              <FormControlLabel
                control={
                  <Switch 
                    checked={preferences.quietHours.enabled}
                    onChange={(e) => handleToggleQuietHours(e.target.checked)}
                  />
                }
                label="Activar horario silencioso para notificaciones push"
              />
              
              {preferences.quietHours.enabled && (
                <Grid container spacing={2} sx={{ mt: 1, pl: 3 }}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Desde"
                      type="time"
                      value={preferences.quietHours.start}
                      onChange={(e) => handleQuietHoursChange('start', e.target.value)}
                      fullWidth
                      InputLabelProps={{ shrink: true }}
                    />
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Hasta"
                      type="time"
                      value={preferences.quietHours.end}
                      onChange={(e) => handleQuietHoursChange('end', e.target.value)}
                      fullWidth
                      InputLabelProps={{ shrink: true }}
                    />
                  </Grid>
                </Grid>
              )}
            </Box>
            
            {devices.length > 0 && (
              <>
                <Divider sx={{ my: 3 }} />
                
                <Typography variant="h6" gutterBottom>Dispositivos Registrados</Typography>
                
                <List>
                  {devices.map(device => (
                    <ListItem 
                      key={device.id}
                      secondaryAction={
                        <IconButton edge="end" onClick={() => handleRemoveDevice(device.id)}>
                          <DeleteIcon />
                        </IconButton>
                      }
                    >
                      <ListItemIcon>
                        {getDeviceIcon(device.platform)}
                      </ListItemIcon>
                      
                      <ListItemText
                        primary={device.name || 'Dispositivo'}
                        secondary={
                          <>
                            <Typography component="span" variant="body2">
                              {getPlatformLabel(device.platform)}
                            </Typography>
                            <Typography component="span" variant="caption" sx={{ ml: 1 }}>
                              Último acceso: {new Date(device.last_active_at).toLocaleString()}
                            </Typography>
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </>
            )}
            
            <Box sx={{ mt: 4, display: 'flex', justifyContent: 'flex-end' }}>
              <Button 
                type="submit" 
                variant="contained" 
                color="primary"
                disabled={saving}
                startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
              >
                {saving ? 'Guardando...' : 'Guardar Preferencias'}
              </Button>
            </Box>
          </form>
        </Paper>
      </MainLayout>
    );
  };
  
  // Función de utilidad para obtener etiqueta descriptiva de tipo
  const getNotificationTypeLabel = (type) => {
    const labels = {
      ACADEMIC: 'Académicas',
      ANNOUNCEMENT: 'Anuncios',
      ALERT: 'Alertas',
      EVENT: 'Eventos',
      MESSAGE: 'Mensajes'
    };
    return labels[type] || type;
  };
  
  // Función de utilidad para obtener icono según plataforma
  const getDeviceIcon = (platform) => {
    switch (platform) {
      case 'android':
        return <AndroidIcon />;
      case 'ios':
        return <AppleIcon />;
      case 'web':
        return <LanguageIcon />;
      default:
        return <DevicesIcon />;
    }
  };
  
  // Función de utilidad para obtener etiqueta de plataforma
  const getPlatformLabel = (platform) => {
    const labels = {
      android: 'Android',
      ios: 'iOS',
      web: 'Navegador Web'
    };
    return labels[platform] || 'Desconocido';
  };
  ```

### 4.7 Configuración

Este módulo permite a los usuarios gestionar sus configuraciones personales, incluyendo perfil, contraseña y preferencias de interfaz.

#### Perfil de Usuario
- **Ruta**: `/profile`
- **Componentes**:
  - `ProfileView`: Vista principal de perfil de usuario
  - `PersonalInfoForm`: Formulario para editar datos personales
  - `PasswordChangeForm`: Formulario para cambiar contraseña
  - `ProfilePictureUploader`: Componente para subir foto de perfil
  - `ActivityHistory`: Historial de actividad reciente
- **Endpoints**:
  - `GET /api/v1/users/me` - Datos del usuario actual
  - `PUT /api/v1/users/me` - Actualizar perfil
  - `PUT /api/v1/users/me/password` - Cambiar contraseña
  - `POST /api/v1/users/me/picture` - Subir foto de perfil
- **Implementación con Template React**:
  ```jsx
  // Componente principal de perfil
  const ProfilePage = () => {
    const [activeTab, setActiveTab] = useState('personal-info');
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { showNotification } = useNotification();
    
    useEffect(() => {
      const fetchUserData = async () => {
        try {
          setLoading(true);
          const response = await api.get('/api/v1/users/me');
          setUserData(response.data);
          setError(null);
        } catch (err) {
          setError('Error al cargar datos de usuario');
          console.error('Error fetching user data:', err);
        } finally {
          setLoading(false);
        }
      };
      
      fetchUserData();
    }, []);
    
    const handleUpdateProfile = async (updatedData) => {
      try {
        const response = await api.put('/api/v1/users/me', updatedData);
        setUserData(response.data);
        showNotification({
          type: 'success',
          message: 'Perfil actualizado correctamente'
        });
        return true;
      } catch (err) {
        console.error('Error updating profile:', err);
        showNotification({
          type: 'error',
          message: 'Error al actualizar perfil'
        });
        return false;
      }
    };
    
    const handlePasswordChange = async (passwordData) => {
      try {
        await api.put('/api/v1/users/me/password', passwordData);
        showNotification({
          type: 'success',
          message: 'Contraseña actualizada correctamente'
        });
        return true;
      } catch (err) {
        console.error('Error changing password:', err);
        showNotification({
          type: 'error',
          message: err.response?.data?.detail || 'Error al cambiar contraseña'
        });
        return false;
      }
    };
    
    const handleProfilePictureUpload = async (file) => {
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await api.post('/api/v1/users/me/picture', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        // Actualizar la URL de la imagen en los datos de usuario
        setUserData(prev => ({
          ...prev,
          profile_picture_url: response.data.profile_picture_url
        }));
        
        showNotification({
          type: 'success',
          message: 'Imagen de perfil actualizada'
        });
        
        return true;
      } catch (err) {
        console.error('Error uploading profile picture:', err);
        showNotification({
          type: 'error',
          message: 'Error al subir imagen de perfil'
        });
        return false;
      }
    };
    
    if (loading) {
      return (
        <MainLayout>
          <ProfileTemplate 
            loading={true}
            title="Perfil de Usuario"
          />
        </MainLayout>
      );
    }
    
    if (error) {
      return (
        <MainLayout>
          <ErrorTemplate 
            message={error}
            retryAction={() => window.location.reload()}
          />
        </MainLayout>
      );
    }
    
    return (
      <MainLayout>
        <ProfileTemplate
          title="Perfil de Usuario"
          userData={userData}
          activeTab={activeTab}
          onTabChange={setActiveTab}
          tabs={[
            {
              id: 'personal-info',
              label: 'Datos Personales',
              icon: <PersonIcon />,
              component: (
                <PersonalInfoForm 
                  userData={userData} 
                  onSubmit={handleUpdateProfile} 
                />
              )
            },
            {
              id: 'password',
              label: 'Cambiar Contraseña',
              icon: <LockIcon />,
              component: (
                <PasswordChangeForm 
                  onSubmit={handlePasswordChange} 
                />
              )
            },
            {
              id: 'profile-picture',
              label: 'Foto de Perfil',
              icon: <PhotoCameraIcon />,
              component: (
                <ProfilePictureUploader 
                  currentImageUrl={userData.profile_picture_url}
                  onUpload={handleProfilePictureUpload}
                />
              )
            },
            {
              id: 'activity',
              label: 'Actividad Reciente',
              icon: <HistoryIcon />,
              component: (
                <ActivityHistory 
                  userId={userData.id}
                />
              )
            }
          ]}
          sidePanel={(
            <ProfileCard 
              user={userData}
              isCurrentUser={true}
            />
          )}
        />
      </MainLayout>
    );
  };
  
  // Template para la página de perfil
  const ProfileTemplate = ({ 
    title, 
    userData, 
    activeTab,
    onTabChange,
    tabs,
    sidePanel,
    loading
  }) => {
    if (loading) {
      return (
        <Box sx={{ p: 3 }}>
          <Skeleton variant="rectangular" height={50} sx={{ mb: 2 }} />
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Skeleton variant="rectangular" height={400} />
            </Grid>
            <Grid item xs={12} md={8}>
              <Skeleton variant="rectangular" height={400} />
            </Grid>
          </Grid>
        </Box>
      );
    }
    
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>{title}</Typography>
        
        <Grid container spacing={3}>
          {/* Panel lateral con información resumida */}
          <Grid item xs={12} md={4}>
            {sidePanel}
          </Grid>
          
          {/* Contenido principal con tabs */}
          <Grid item xs={12} md={8}>
            <Paper elevation={2} sx={{ p: 0 }}>
              <Tabs 
                value={activeTab} 
                onChange={(e, newValue) => onTabChange(newValue)}
                variant="scrollable"
                scrollButtons="auto"
              >
                {tabs.map(tab => (
                  <Tab 
                    key={tab.id}
                    value={tab.id}
                    label={tab.label}
                    icon={tab.icon}
                    iconPosition="start"
                  />
                ))}
              </Tabs>
              
              <Box sx={{ p: 3 }}>
                {tabs.find(tab => tab.id === activeTab)?.component}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  };
  
  // Componente para el formulario de información personal
  const PersonalInfoForm = ({ userData, onSubmit }) => {
    const [formData, setFormData] = useState({
      full_name: userData.full_name || '',
      email: userData.email || '',
      phone: userData.phone || '',
      biography: userData.biography || ''
    });
    const [submitting, setSubmitting] = useState(false);
    
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData(prev => ({ ...prev, [name]: value }));
    };
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      setSubmitting(true);
      
      const success = await onSubmit(formData);
      
      setSubmitting(false);
    };
    
    return (
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              label="Nombre Completo"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              fullWidth
              required
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              label="Email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              fullWidth
              required
              type="email"
              disabled // El email normalmente no se puede cambiar
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              label="Teléfono"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              fullWidth
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              label="Biografía"
              name="biography"
              value={formData.biography}
              onChange={handleChange}
              fullWidth
              multiline
              rows={4}
            />
          </Grid>
          
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={submitting}
              startIcon={submitting ? <CircularProgress size={20} /> : <SaveIcon />}
            >
              {submitting ? 'Guardando...' : 'Guardar Cambios'}
            </Button>
          </Grid>
        </Grid>
      </form>
    );
  };
  ```

#### Preferencias de Interfaz
- **Ruta**: `/settings/interface`
- **Componentes**:
  - `InterfaceSettingsForm`: Formulario para configuraciones de interfaz
  - `ThemeSelector`: Selector de tema (claro/oscuro/sistema)
  - `LanguageSelector`: Selector de idioma
  - `AccessibilitySettings`: Configuraciones de accesibilidad
- **Endpoints**:
  - `GET /api/v1/users/me/preferences` - Obtener preferencias
  - `PUT /api/v1/users/me/preferences` - Actualizar preferencias
- **Implementación con Template React**:
  ```jsx
  const InterfaceSettingsPage = () => {
    const [preferences, setPreferences] = useState({
      theme: 'system', // 'light', 'dark', 'system'
      language: 'es', // 'es', 'en', etc.
      fontSize: 'medium', // 'small', 'medium', 'large'
      highContrast: false,
      reducedMotion: false,
      autoplayVideos: true,
      compactView: false
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const { setTheme } = useTheme(); // Hook para cambiar el tema
    const { setLanguage } = useLanguage(); // Hook para cambiar el idioma
    const { showNotification } = useNotification();
    
    useEffect(() => {
      const fetchPreferences = async () => {
        try {
          setLoading(true);
          const response = await api.get('/api/v1/users/me/preferences');
          if (response.data && response.data.interface) {
            setPreferences(response.data.interface);
          }
        } catch (error) {
          console.error('Error fetching preferences:', error);
          // Si hay error, mantener valores por defecto
        } finally {
          setLoading(false);
        }
      };
      
      fetchPreferences();
    }, []);
    
    // Cuando cambia el tema en las preferencias, actualizamos el tema de la aplicación
    useEffect(() => {
      if (!loading) {
        setTheme(preferences.theme);
        setLanguage(preferences.language);
      }
    }, [preferences.theme, preferences.language, loading, setTheme, setLanguage]);
    
    const handleChange = (name, value) => {
      setPreferences(prev => ({
        ...prev,
        [name]: value
      }));
    };
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      setSaving(true);
      
      try {
        await api.put('/api/v1/users/me/preferences', {
          interface: preferences
        });
        
        showNotification({
          type: 'success',
          message: 'Preferencias guardadas correctamente'
        });
      } catch (error) {
        console.error('Error saving preferences:', error);
        showNotification({
          type: 'error',
          message: 'Error al guardar preferencias'
        });
      } finally {
        setSaving(false);
      }
    };
    
    if (loading) {
      return (
        <MainLayout>
          <SettingsTemplate 
            title="Preferencias de Interfaz"
            loading={true}
          />
        </MainLayout>
      );
    }
    
    return (
      <MainLayout>
        <SettingsTemplate
          title="Preferencias de Interfaz"
          icon={<DisplaySettingsIcon />}
          content={
            <form onSubmit={handleSubmit}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Apariencia</Typography>
                  
                  <FormControl fullWidth margin="normal">
                    <FormLabel id="theme-label">Tema</FormLabel>
                    <RadioGroup 
                      aria-labelledby="theme-label"
                      value={preferences.theme}
                      onChange={(e) => handleChange('theme', e.target.value)}
                      row
                    >
                      <FormControlLabel value="light" control={<Radio />} label="Claro" />
                      <FormControlLabel value="dark" control={<Radio />} label="Oscuro" />
                      <FormControlLabel value="system" control={<Radio />} label="Sistema" />
                    </RadioGroup>
                  </FormControl>
                  
                  <FormControl fullWidth margin="normal">
                    <InputLabel id="language-label">Idioma</InputLabel>
                    <Select
                      labelId="language-label"
                      value={preferences.language}
                      onChange={(e) => handleChange('language', e.target.value)}
                    >
                      <MenuItem value="es">Español</MenuItem>
                      <MenuItem value="en">English</MenuItem>
                    </Select>
                  </FormControl>
                  
                  <FormControl fullWidth margin="normal">
                    <FormLabel id="font-size-label">Tamaño de Texto</FormLabel>
                    <RadioGroup 
                      aria-labelledby="font-size-label"
                      value={preferences.fontSize}
                      onChange={(e) => handleChange('fontSize', e.target.value)}
                      row
                    >
                      <FormControlLabel value="small" control={<Radio />} label="Pequeño" />
                      <FormControlLabel value="medium" control={<Radio />} label="Mediano" />
                      <FormControlLabel value="large" control={<Radio />} label="Grande" />
                    </RadioGroup>
                  </FormControl>
                </CardContent>
              </Card>
              
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Accesibilidad</Typography>
                  
                  <FormControlLabel
                    control={
                      <Switch 
                        checked={preferences.highContrast}
                        onChange={(e) => handleChange('highContrast', e.target.checked)}
                      />
                    }
                    label="Alto contraste"
                  />
                  
                  <FormControlLabel
                    control={
                      <Switch 
                        checked={preferences.reducedMotion}
                        onChange={(e) => handleChange('reducedMotion', e.target.checked)}
                      />
                    }
                    label="Reducir movimiento"
                  />
                </CardContent>
              </Card>
              
              <Card sx={{ mt: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Rendimiento</Typography>
                  
                  <FormControlLabel
                    control={
                      <Switch 
                        checked={preferences.autoplayVideos}
                        onChange={(e) => handleChange('autoplayVideos', e.target.checked)}
                      />
                    }
                    label="Reproducir videos automáticamente"
                  />
                  
                  <FormControlLabel
                    control={
                      <Switch 
                        checked={preferences.compactView}
                        onChange={(e) => handleChange('compactView', e.target.checked)}
                      />
                    }
                    label="Vista compacta"
                  />
                </CardContent>
              </Card>
              
              <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  disabled={saving}
                  startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
                >
                  {saving ? 'Guardando...' : 'Guardar Preferencias'}
                </Button>
              </Box>
            </form>
          }
        />
      </MainLayout>
    );
  };
  
  // Template para páginas de configuración
  const SettingsTemplate = ({ title, icon, content, loading }) => {
    if (loading) {
      return (
        <Box sx={{ p: 3 }}>
          <Skeleton variant="rectangular" height={50} sx={{ mb: 2 }} />
          <Skeleton variant="rectangular" height={400} />
        </Box>
      );
    }
    
    return (
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          {icon && <Box sx={{ mr: 1 }}>{icon}</Box>}
          <Typography variant="h4">{title}</Typography>
        </Box>
        
        {content}
      </Box>
    );
  };
  ```

#### Gestión de Dispositivos
- **Ruta**: `/devices`
- **Componentes**:
  - `DevicesManager`: Componente principal para gestionar dispositivos
  - `DevicesList`: Listado de dispositivos registrados
  - `DeviceCard`: Tarjeta con información y acciones de un dispositivo
  - `AddDeviceModal`: Modal para agregar un nuevo dispositivo
  - `ConfirmRemovalDialog`: Diálogo de confirmación para eliminar dispositivo
- **Endpoints**:
  - `GET /api/v1/devices` - Listar dispositivos del usuario
  - `POST /api/v1/devices` - Registrar nuevo dispositivo
  - `DELETE /api/v1/devices/{device_id}` - Eliminar dispositivo
  - `PUT /api/v1/devices/{device_id}` - Actualizar nombre o estado de dispositivo
- **Implementación con Template React**:
  ```jsx
  const DevicesManagerPage = () => {
    const [devices, setDevices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [addDeviceOpen, setAddDeviceOpen] = useState(false);
    const [deviceToRemove, setDeviceToRemove] = useState(null);
    const [removeDialogOpen, setRemoveDialogOpen] = useState(false);
    const { showNotification } = useNotification();
    
    useEffect(() => {
      fetchDevices();
    }, []);
    
    const fetchDevices = async () => {
      setLoading(true);
      try {
        const response = await api.get('/api/v1/devices');
        setDevices(response.data || []);
      } catch (error) {
        console.error('Error fetching devices:', error);
        showNotification({
          type: 'error',
          message: 'Error al cargar dispositivos'
        });
      } finally {
        setLoading(false);
      }
    };
    
    const handleAddDevice = async (deviceData) => {
      try {
        const response = await api.post('/api/v1/devices', deviceData);
        setDevices(prev => [...prev, response.data]);
        showNotification({
          type: 'success',
          message: 'Dispositivo agregado correctamente'
        });
        setAddDeviceOpen(false);
        return true;
      } catch (error) {
        console.error('Error adding device:', error);
        showNotification({
          type: 'error',
          message: 'Error al agregar dispositivo'
        });
        return false;
      }
    };
    
    const handleUpdateDevice = async (deviceId, updates) => {
      try {
        const response = await api.put(`/api/v1/devices/${deviceId}`, updates);
        setDevices(prev => prev.map(device => 
          device.id === deviceId ? { ...device, ...response.data } : device
        ));
        showNotification({
          type: 'success',
          message: 'Dispositivo actualizado correctamente'
        });
        return true;
      } catch (error) {
        console.error('Error updating device:', error);
        showNotification({
          type: 'error',
          message: 'Error al actualizar dispositivo'
        });
        return false;
      }
    };
    
    const openRemoveDialog = (device) => {
      setDeviceToRemove(device);
      setRemoveDialogOpen(true);
    };
    
    const handleRemoveDevice = async () => {
      if (!deviceToRemove) return;
      
      try {
        await api.delete(`/api/v1/devices/${deviceToRemove.id}`);
        setDevices(prev => prev.filter(d => d.id !== deviceToRemove.id));
        showNotification({
          type: 'success',
          message: 'Dispositivo eliminado correctamente'
        });
        setRemoveDialogOpen(false);
        setDeviceToRemove(null);
      } catch (error) {
        console.error('Error removing device:', error);
        showNotification({
          type: 'error',
          message: 'Error al eliminar dispositivo'
        });
      }
    };
    
    // Template para la vista de dispositivos
    return (
      <MainLayout>
        <DevicesTemplate
          title="Gestionar Dispositivos"
          loading={loading}
          devices={devices}
          onAddDevice={() => setAddDeviceOpen(true)}
          onUpdateDevice={handleUpdateDevice}
          onRemoveDevice={openRemoveDialog}
          emptyMessage="No tienes dispositivos registrados"
          emptyActionText="Registrar Dispositivo"
        />
        
        {/* Modal para agregar dispositivo */}
        <AddDeviceModal 
          open={addDeviceOpen}
          onClose={() => setAddDeviceOpen(false)}
          onAdd={handleAddDevice}
        />
        
        {/* Diálogo de confirmación para eliminar */}
        <ConfirmDialog
          open={removeDialogOpen}
          title="Eliminar Dispositivo"
          content={`¿Estás seguro de que deseas eliminar el dispositivo ${deviceToRemove?.name || ''}? Esta acción no se puede deshacer.`}
          confirmText="Eliminar"
          cancelText="Cancelar"
          onConfirm={handleRemoveDevice}
          onCancel={() => {
            setRemoveDialogOpen(false);
            setDeviceToRemove(null);
          }}
          confirmColor="error"
        />
      </MainLayout>
    );
  };
  
  // Template para la página de dispositivos
  const DevicesTemplate = ({
    title,
    loading,
    devices,
    onAddDevice,
    onUpdateDevice,
    onRemoveDevice,
    emptyMessage,
    emptyActionText
  }) => {
    if (loading) {
      return (
        <Box sx={{ p: 3 }}>
          <Typography variant="h4" gutterBottom>{title}</Typography>
          <DevicesListSkeleton count={3} />
        </Box>
      );
    }
    
    return (
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">{title}</Typography>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={onAddDevice}
          >
            Agregar Dispositivo
          </Button>
        </Box>
        
        {devices.length > 0 ? (
          <Grid container spacing={3}>
            {devices.map(device => (
              <Grid item xs={12} sm={6} md={4} key={device.id}>
                <DeviceCard 
                  device={device}
                  onUpdate={(updates) => onUpdateDevice(device.id, updates)}
                  onRemove={() => onRemoveDevice(device)}
                />
              </Grid>
            ))}
          </Grid>
        ) : (
          <EmptyState
            icon={<DevicesIcon sx={{ fontSize: 64 }} />}
            message={emptyMessage}
            actionText={emptyActionText}
            onAction={onAddDevice}
          />
        )}
      </Box>
    );
  };
  
  // Componente de tarjeta de dispositivo
  const DeviceCard = ({ device, onUpdate, onRemove }) => {
    const [editing, setEditing] = useState(false);
    const [name, setName] = useState(device.name || 'Dispositivo');
    
    const handleNameChange = (e) => {
      setName(e.target.value);
    };
    
    const handleSave = async () => {
      if (name.trim() === '') return;
      
      const success = await onUpdate({ name: name.trim() });
      if (success) {
        setEditing(false);
      }
    };
    
    const handleToggleActive = async () => {
      await onUpdate({ active: !device.active });
    };
    
    return (
      <Card>
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: device.active ? 'success.main' : 'text.disabled' }}>
              {getDeviceIcon(device.platform)}
            </Avatar>
          }
          action={
            <IconButton aria-label="settings" onClick={onRemove}>
              <DeleteIcon />
            </IconButton>
          }
          title={
            editing ? (
              <TextField 
                value={name}
                onChange={handleNameChange}
                size="small"
                autoFocus
                fullWidth
                onKeyDown={(e) => e.key === 'Enter' && handleSave()}
              />
            ) : (
              device.name || 'Dispositivo'
            )
          }
          subheader={getPlatformLabel(device.platform)}
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Último acceso: {new Date(device.last_active_at).toLocaleString()}
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
            <Typography variant="body2" sx={{ mr: 1 }}>
              Estado:
            </Typography>
            <Chip 
              label={device.active ? 'Activo' : 'Inactivo'}
              color={device.active ? 'success' : 'default'}
              size="small"
            />
          </Box>
        </CardContent>
        <CardActions sx={{ justifyContent: 'space-between' }}>
          {editing ? (
            <>
              <Button size="small" onClick={() => setEditing(false)}>Cancelar</Button>
              <Button size="small" color="primary" onClick={handleSave}>Guardar</Button>
            </>
          ) : (
            <>
              <Button size="small" onClick={() => setEditing(true)} startIcon={<EditIcon />}>Editar</Button>
              <Button 
                size="small" 
                color={device.active ? 'error' : 'success'}
                onClick={handleToggleActive}
              >
                {device.active ? 'Desactivar' : 'Activar'}
              </Button>
            </>
          )}
        </CardActions>
      </Card>
    );
  };
  
  // Componente modal para agregar dispositivo
  const AddDeviceModal = ({ open, onClose, onAdd }) => {
    const [formData, setFormData] = useState({
      name: '',
      platform: 'web',
      token: ''
    });
    const [submitting, setSubmitting] = useState(false);
    
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData(prev => ({ ...prev, [name]: value }));
    };
    
    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!formData.name.trim() || !formData.platform) return;
      
      setSubmitting(true);
      const success = await onAdd(formData);
      setSubmitting(false);
      
      if (success) {
        setFormData({
          name: '',
          platform: 'web',
          token: ''
        });
      }
    };
    
    return (
      <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
        <DialogTitle>Agregar Nuevo Dispositivo</DialogTitle>
        <DialogContent>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            <TextField
              label="Nombre del Dispositivo"
              name="name"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              required
              margin="normal"
            />
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="platform-label">Plataforma</InputLabel>
              <Select
                labelId="platform-label"
                name="platform"
                value={formData.platform}
                onChange={handleChange}
              >
                <MenuItem value="web">Navegador Web</MenuItem>
                <MenuItem value="android">Android</MenuItem>
                <MenuItem value="ios">iOS</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              label="Token de Dispositivo (opcional)"
              name="token"
              value={formData.token}
              onChange={handleChange}
              fullWidth
              margin="normal"
              helperText="Para recibir notificaciones push"
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancelar</Button>
          <Button 
            onClick={handleSubmit} 
            color="primary" 
            disabled={submitting || !formData.name.trim()}
          >
            {submitting ? <CircularProgress size={24} /> : 'Agregar'}
          </Button>
        </DialogActions>
      </Dialog>
    );
  };
  
  // Componente para mostrar esqueleto de carga
  const DevicesListSkeleton = ({ count }) => {
    return (
      <Grid container spacing={3}>
        {Array.from(new Array(count)).map((_, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardHeader
                avatar={<Skeleton variant="circular" width={40} height={40} />}
                title={<Skeleton width="80%" />}
                subheader={<Skeleton width="40%" />}
              />
              <CardContent>
                <Skeleton width="90%" />
                <Skeleton width="60%" />
              </CardContent>
              <CardActions>
                <Skeleton width={80} height={40} />
                <Skeleton width={80} height={40} />
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  };
  ```

### 4.8 Módulos Adicionales

Además de los módulos principales detallados anteriormente, el sistema cuenta con los siguientes módulos adicionales o de soporte:

#### Calendario Académico
- **Ruta**: `/calendar`
- **Componentes**:
  - `CalendarView`: Vista principal del calendario
  - `EventDetails`: Detalles de un evento
  - `CreateEventForm`: Formulario para crear eventos (solo admin/profesor)
  - `FilterControls`: Controles para filtrar eventos por tipo y curso
- **Endpoints**:
  - `GET /api/v1/calendar/events` - Listar eventos del calendario
  - `POST /api/v1/calendar/events` - Crear nuevo evento (admin/profesor)
  - `GET /api/v1/calendar/events/{event_id}` - Obtener detalles de evento
  - `PUT /api/v1/calendar/events/{event_id}` - Actualizar evento

#### Búsqueda Global
- **Ruta**: Componente global en header
- **Componentes**:
  - `GlobalSearch`: Campo de búsqueda principal
  - `SearchResults`: Resultados de búsqueda por categoría
  - `QuickAccess`: Accesos rápidos personalizados
- **Endpoints**:
  - `GET /api/v1/search` - Búsqueda global en todo el sistema
  - `GET /api/v1/quick-access` - Accesos rápidos configurados por el usuario

#### Ayuda y Soporte
- **Ruta**: `/help`
- **Componentes**:
  - `HelpCenter`: Centro de ayuda con documentación
  - `FAQSection`: Preguntas frecuentes por categoría
  - `SupportTicketForm`: Formulario para enviar tickets de soporte
  - `KnowledgeBase`: Base de conocimientos y tutoriales
- **Endpoints**:
  - `GET /api/v1/help/faqs` - Obtener preguntas frecuentes
  - `POST /api/v1/help/tickets` - Crear ticket de soporte
  - `GET /api/v1/help/articles` - Obtener artículos de ayuda

## 5. Patrones de Diseño y Mejores Prácticas

### 5.1 Patrones de Diseño UI/UX

#### Sistema de Templates
Para mantener la consistencia visual y funcional en toda la aplicación, se implementará un sistema de templates React con los siguientes componentes base:

- **MainLayout**: Layout principal con header, navigation drawer y footer
- **PageTemplate**: Template base para páginas estándar con título, acciones y contenido
- **ListTemplate**: Template para páginas de listado con filtros, paginación y acciones
- **DetailTemplate**: Template para páginas de detalle con navegación de regreso
- **FormTemplate**: Template para páginas con formularios extensos
- **DashboardTemplate**: Template para dashboards con gráficos y estadísticas

#### Componentes Compartidos

- **ActionButton**: Botón estándar para acciones principales
- **FilterPanel**: Panel unificado para filtros en listados
- **Pagination**: Componente de paginación estándar
- **StatusChip**: Chip para mostrar estados con colores semánticos
- **EmptyState**: Estado vacío para listas sin contenido
- **ErrorState**: Estado de error con opción de reintentar
- **LoadingIndicator**: Indicador de carga estándar
- **ConfirmDialog**: Diálogo de confirmación para acciones destructivas

### 5.2 Estrategias de Estado

- **Estados Locales**: React useState para estados de componentes locales
- **Estados Globales**: React Context para temas como autenticación, notificaciones y preferencias
- **Manejo de Formularios**: React Hook Form para validación y gestión de formularios
- **Gestión de Errores**: Sistema centralizado de captación y presentación de errores

### 5.3 Estrategias de Rendimiento

- **Lazy Loading**: Carga diferida de componentes y rutas mediante React.lazy y Suspense
- **Paginación y Filtrado**: Implementación de paginación y filtrado del lado del servidor
- **Memoización**: Uso de React.memo, useMemo y useCallback para optimizar renderizados
- **Virtualización**: Para listas largas, uso de react-window o react-virtualized

### 5.4 Accesibilidad

- **Semántica HTML**: Uso correcto de elementos semánticos (heading levels, landmarks)
- **ARIA**: Implementación de atributos ARIA donde sea necesario
- **Navegación por Teclado**: Asegurar que todos los elementos interactivos sean accesibles por teclado
- **Contraste**: Garantizar suficiente contraste de color
- **Tamaño de Texto Configurable**: Permitir al usuario ajustar el tamaño del texto

## 6. Consideraciones de Implementación

### 6.1 Tecnologías Frontend

- **Framework**: React JS con templates personalizados
- **UI Library**: Material-UI (MUI) para componentes base
- **Routing**: React Router para navegación
- **Estado Global**: React Context API para estados globales como autenticación
- **Formularios**: React Hook Form para manejo de formularios
- **HTTP Client**: Axios para comunicación con el backend
- **Internacionalización**: i18next para soporte multi-idioma

### 6.2 Integración con Backend

- **API REST**: Comunicación con el backend mediante API REST
- **Interceptores**: Configuración de interceptores para manejo de tokens y errores
- **Caché**: Implementación de caché para optimizar rendimiento
- **Websockets**: Para notificaciones en tiempo real

### 6.3 Seguridad

- **JWT**: Almacenamiento seguro de tokens JWT
- **CSRF**: Protección contra CSRF
- **XSS**: Prevención de ataques XSS
- **RBAC**: Control de acceso basado en roles implementado en frontend

### 6.4 Testing

- **Unit Testing**: Jest para pruebas unitarias
- **Component Testing**: React Testing Library para pruebas de componentes
- **E2E Testing**: Cypress para pruebas end-to-end
- **A11y Testing**: jest-axe para pruebas de accesibilidad
- **Endpoints**:
  - `GET /api/v1/devices` - Dispositivos registrados
  - `POST /api/v1/devices` - Registrar nuevo dispositivo
  - `DELETE /api/v1/devices/{device_id}` - Eliminar dispositivo

## 5. Diseño Detallado de Módulos

Esta sección profundiza en el diseño específico de cada módulo, incluyendo descripciones detalladas de cómo deberían construirse las vistas, patrones de diseño recomendados y mejores prácticas de implementación.

### 5.1 Principios de Diseño General

#### Layouts Adaptativos
Cada módulo debe implementarse con un enfoque de diseño adaptativo que considere tres estados principales:

1. **Vista Desktop (> 1024px)**
   - Navegación lateral siempre visible
   - Paneles múltiples simultáneos
   - Vista completa de tablas y datos

2. **Vista Tablet (768px - 1024px)**
   - Navegación lateral colapsable
   - Disposición de contenido en dos columnas cuando sea posible
   - Tablas con scroll horizontal para datos extensos

3. **Vista Móvil (< 768px)**
   - Navegación en menú hamburguesa
   - Diseño de una sola columna
   - Acciones principales siempre visibles
   - Tabs para cambiar entre secciones relacionadas

#### Componentes Consistentes
Cada módulo debe utilizar un conjunto coherente de componentes que mantengan la consistencia visual y de interacción:

- **AppBars**: Consistentes en toda la aplicación, con variaciones contextuales
- **Cards**: Con variantes para datos, acciones, estadísticas y contenido multimedia
- **Forms**: Patrones consistentes de validación, feedback y acciones
- **Tables**: Con comportamientos unificados para ordenamiento, filtrado y paginación

### 5.2 Patrones de Diseño Modernos

#### 1. Component Composition Pattern
Utilizar composición de componentes pequeños y especializados para construir interfaces complejas:

```jsx
// Ejemplo conceptual
<StudentCard>
  <CardHeader>
    <Avatar src={student.photo} />
    <StudentInfo name={student.name} id={student.code} />
  </CardHeader>
  <CardBody>
    <GradesSummary grades={student.grades} />
    <AttendanceSummary attendance={student.attendance} />
  </CardBody>
  <CardActions>
    <ActionButton icon="edit" onClick={handleEdit} />
    <ActionButton icon="message" onClick={handleMessage} />
  </CardActions>
</StudentCard>
```

#### 2. Container/Presentational Pattern
Separar la lógica de estado y datos (containers) de la presentación visual (componentes):

```jsx
// Container Component (maneja datos y lógica)
const StudentGradesContainer = () => {
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStudentGrades(studentId)
      .then(data => setGrades(data))
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, [studentId]);

  return (
    <StudentGradesView 
      grades={grades} 
      loading={loading} 
      error={error} 
    />
  );
};

// Presentational Component (solo UI)
const StudentGradesView = ({ grades, loading, error }) => {
  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error.message} />;
  
  return (
    <GradesTable data={grades} />
  );
};
```

#### 3. Render Props & Compound Components
Componentes flexibles que permiten personalización de comportamiento y apariencia:

```jsx
// Render Props Example
<DataFetcher 
  endpoint="/api/v1/grades/student/123" 
  render={(data, loading, error) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage message={error.message} />;
    return <GradesChart data={data} />;
  }} 
/>

// Compound Components Example
<Tabs defaultActiveKey="grades">
  <Tab key="grades" title="Calificaciones">
    <GradesPanel studentId={123} />
  </Tab>
  <Tab key="attendance" title="Asistencia">
    <AttendancePanel studentId={123} />
  </Tab>
  <Tab key="behavior" title="Comportamiento">
    <BehaviorPanel studentId={123} />
  </Tab>
</Tabs>
```

#### 4. State Machines para Flujos Complejos
Utilizar máquinas de estado (con XState o implementaciones similares) para manejar flujos complejos:

```jsx
// Ejemplo conceptual de máquina de estado para matrícula
const enrollmentMachine = createMachine({
  id: 'enrollment',
  initial: 'selectStudent',
  states: {
    selectStudent: {
      on: { NEXT: 'selectCourses' }
    },
    selectCourses: {
      on: { NEXT: 'reviewPayment', BACK: 'selectStudent' }
    },
    reviewPayment: {
      on: { NEXT: 'processPayment', BACK: 'selectCourses' }
    },
    processPayment: {
      on: { PAYMENT_SUCCESS: 'complete', PAYMENT_FAILURE: 'paymentError' }
    },
    paymentError: {
      on: { RETRY: 'processPayment', BACK: 'reviewPayment' }
    },
    complete: {
      type: 'final'
    }
  }
});
```

### 5.3 Diseño Detallado por Módulo

#### Autenticación

**Login**
- Implementar diseño de split-screen:
  - Mitad izquierda: formulario de login minimalista
  - Mitad derecha: imagen institucional o ilustración relacionada con educación
- Incluir acciones secundarias (recuperar contraseña, registro) como enlaces discretos
- Implementar validación en tiempo real con feedback visual inmediato
- Mostrar mensajes de error específicos y orientados a soluciones

**Recuperación de Contraseña**
- Implementar como flujo guiado paso a paso (wizard pattern)
- Indicador de progreso visual para mostrar etapa actual
- Confirmaciones visuales para cada acción completada

#### Dashboard

**Estructura General**
- Implementar sistema de widgets configurables:
  - Arrastrar y soltar para personalizar (drag-and-drop)
  - Widgets colapsables y expandibles
  - Configuración de preferencias persistente

**Dashboard Estudiante**
- Widget principal: Resumen de calificaciones con gráfico radar por criterios
- Widget secundario: Calendario con próximas entregas y eventos
- Widget terciario: Asistencia con indicadores visuales de tendencia
- Sección de notificaciones recientes con acciones rápidas

```jsx
<DashboardLayout>
  <DashboardHeader title="Dashboard Estudiante" user={currentUser} />
  <WidgetGrid>
    <Widget size="large" title="Rendimiento Académico">
      <GradesRadarChart data={gradesData} />
      <GradesTrendLine data={gradesHistory} />
    </Widget>
    
    <Widget size="medium" title="Próximas Actividades">
      <EventTimeline events={upcomingEvents} />
    </Widget>
    
    <Widget size="medium" title="Asistencia">
      <AttendanceCalendar data={attendanceData} />
      <AttendanceStats percentage={attendancePercentage} />
    </Widget>
    
    <Widget size="small" title="Notificaciones">
      <NotificationList 
        items={recentNotifications} 
        onItemClick={handleNotificationClick} 
      />
    </Widget>
  </WidgetGrid>
</DashboardLayout>
```

**Dashboard Profesor**
- Vista principal: Matriz de cursos asignados con indicadores de estado
- Sección de actividades pendientes (calificaciones, asistencias)
- Análisis rápido de rendimiento por curso con visualizaciones
- Accesos directos a acciones frecuentes (registrar asistencia, calificar)

#### Gestión Académica

**Listado de Cursos**
- Implementar vista de tarjetas para cursos con información visual relevante:
  - Código de colores por materia
  - Indicadores de progreso circular
  - Contadores de estudiantes y actividades
- Incluir filtros rápidos por período, nivel y estado
- Implementar búsqueda con sugerencias y resultados instantáneos

**Calificaciones**
- Estructura de datos jerárquica con expansión progresiva:
  - Nivel 1: Resumen por criterio principal (to_be, to_know, etc.)
  - Nivel 2: Detalle de actividades por criterio
  - Nivel 3: Desglose de subcriterios y rúbricas
- Editor de calificaciones inline con validación contextual
- Visualizaciones comparativas (distribuciones, promedios, percentiles)

```jsx
<GradesModule>
  <FilterToolbar
    periods={availablePeriods}
    criteria={evaluationCriteria}
    onFilterChange={handleFilterChange}
  />
  
  <GradesTable
    data={filteredGrades}
    expandable={true}
    editable={userCanEdit}
    onGradeChange={handleGradeChange}
    renderCustomCell={(column, row) => {
      if (column === 'progress') {
        return <ProgressIndicator value={row.progress} />;
      }
      return null;
    }}
  />
  
  <GradesInsights data={gradesStatistics}>
    <DistributionChart />
    <TrendAnalysis />
    <ComparisonMetrics />
  </GradesInsights>
</GradesModule>
```

#### Comunidad Educativa

**Directorio de Estudiantes**
- Implementar vista dual:
  - Vista de tarjetas con fotos e información esencial
  - Vista de tabla detallada con ordenamiento y filtros avanzados
- Búsqueda con filtros combinados (grupo, nivel, estado académico)
- Sistema de etiquetas visuales para indicar situaciones especiales

**Perfil de Estudiante**
- Diseño de tabs verticales para secciones principales:
  - Información personal y académica
  - Historial de calificaciones
  - Registro de asistencia
  - Comunicaciones y notificaciones
- Timeline vertical para eventos académicos importantes
- Tarjetas de métricas clave con comparativas y tendencias

#### Sistema de Notificaciones

**Centro de Notificaciones**
- Diseño de lista priorizada con código de colores por tipo y urgencia
- Agrupación inteligente de notificaciones relacionadas
- Controles de filtrado rápido con contadores visuales
- Acciones en lote para gestión eficiente

```jsx
<NotificationCenter>
  <NotificationFilters
    types={notificationTypes}
    priorities={priorityLevels}
    onFilterChange={handleFilterChange}
    counts={filterCounts}
  />
  
  <NotificationList>
    {notifications.map(notification => (
      <NotificationItem
        key={notification.id}
        data={notification}
        isRead={notification.is_read}
        priority={notification.priority}
        actions={[
          { label: 'Marcar como leída', onClick: () => markAsRead(notification.id) },
          { label: 'Eliminar', onClick: () => deleteNotification(notification.id) },
          { label: 'Ver detalles', onClick: () => viewDetails(notification.id) },
        ]}
      />
    ))}
  </NotificationList>
  
  <NotificationBatchActions
    selectedCount={selectedNotifications.length}
    onMarkAllRead={handleMarkAllRead}
    onDeleteSelected={handleDeleteSelected}
  />
</NotificationCenter>
```

### 5.4 Patrones de Micro-Interacción

#### Feedback Visual Instantáneo
Implementar respuestas visuales inmediatas para todas las acciones del usuario:

- **Botones**: Estados hover, active, focus y disabled visualmente distintos
- **Inputs**: Validación visual en tiempo real con códigos de color e iconos
- **Acciones**: Confirmación visual de éxito/error con mensajes contextuales
- **Transiciones**: Animaciones sutiles para cambios de estado (300-500ms)

#### Skeleton Screens
Reemplazar spinners tradicionales con esqueletos de contenido durante la carga:

```jsx
const StudentCard = ({ student, loading }) => {
  if (loading) {
    return (
      <Card>
        <Skeleton variant="circular" width={40} height={40} />
        <Skeleton variant="text" width="80%" height={20} />
        <Skeleton variant="text" width="60%" height={20} />
        <Skeleton variant="rectangular" width="100%" height={60} />
      </Card>
    );
  }
  
  return (
    <Card>
      <Avatar src={student.photo} />
      <Typography variant="h6">{student.name}</Typography>
      <Typography variant="body2">{student.code}</Typography>
      <GradesSummary grades={student.grades} />
    </Card>
  );
};
```

#### Empty States Diseñados
Estados vacíos informativos y accionables en lugar de mensajes genéricos:

```jsx
const NotificationsList = ({ notifications }) => {
  if (notifications.length === 0) {
    return (
      <EmptyState
        illustration={<NotificationIllustration />}
        title="No tienes notificaciones pendientes"
        description="Las notificaciones importantes aparecerán aquí"
        action={{
          label: "Ajustar preferencias",
          onClick: handleOpenPreferences
        }}
      />
    );
  }
  
  return (
    <List>
      {notifications.map(notification => (
        <NotificationItem key={notification.id} data={notification} />
      ))}
    </List>
  );
};
```

### 5.5 Mejores Prácticas de Implementación

#### Composición Funcional
- Preferir composición sobre herencia para reutilizar código
- Utilizar hooks personalizados para lógica compartida
- Implementar High Order Components (HOC) para comportamientos transversales

#### Estrategias de Rendering
- Implementar técnicas de memorización (useMemo, useCallback, React.memo)
- Utilizar virtualización para listas largas (react-window, react-virtualized)
- Implementar lazy loading para código y datos

#### Arquitectura de Datos
- Normalizar datos complejos en el cliente
- Implementar cache local para consultas frecuentes
- Utilizar optimistic updates para experiencia fluida

## 6. Consideraciones Técnicas

### Autenticación y Seguridad
- Implementar JWT para la autenticación
- Almacenar tokens en localStorage/sessionStorage según las necesidades de seguridad
- Manejar la renovación automática de tokens
- Implementar protección de rutas basada en roles

### Gestión de Estado
- Utilizar un store centralizado para:
  - Estado de autenticación
  - Datos de usuario actual
  - Notificaciones
  - Datos compartidos entre componentes

### Optimización de Rendimiento
- Implementar carga perezosa (lazy loading) de módulos
- Utilizar memorización para componentes y consultas costosas
- Implementar paginación y carga infinita para listas grandes
- Optimizar imágenes y recursos estáticos

### Accesibilidad y Diseño Responsivo
- Seguir directrices WCAG 2.1 para accesibilidad
- Implementar diseño mobile-first
- Utilizar breakpoints estándar para diferentes dispositivos
- Probar en múltiples tamaños de pantalla y dispositivos

### Comunicación en Tiempo Real
- Implementar WebSockets para notificaciones en tiempo real
- Considerar la implementación de actualización en tiempo real para:
  - Notificaciones
  - Calificaciones recientes
  - Asistencia
  - Chat (si se implementa)

### Gestión de Errores
- Implementar un sistema centralizado de manejo de errores
- Mostrar mensajes de error amigables al usuario
- Registrar errores para análisis posterior
- Implementar reintentos automáticos para peticiones fallidas cuando sea apropiado

### Internacionalización
- Implementar soporte para múltiples idiomas
- Separar textos en archivos de traducción
- Considerar aspectos culturales en formatos de fecha y números
