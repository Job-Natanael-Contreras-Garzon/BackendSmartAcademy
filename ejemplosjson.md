# Ejemplos de Peticiones JSON para Smart Academy API

Este documento contiene ejemplos de peticiones JSON para los endpoints de la API, así como sus respectivas respuestas. Utilice estos ejemplos para realizar pruebas y entender cómo interactuar con la API.

## 1. Autenticación

### 1.1. Login (/api/v1/auth/login)

**Método**: POST

**Request:**
```json
{
  "email": "admin@smartacademy.com",
  "password": "admin123"
}
```

**Response Exitosa (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "admin@smartacademy.com",
  "full_name": "Administrador",
  "role": "administrator",
  "is_superuser": true
}
```

**Response Fallida (401 Unauthorized):**
```json
{
  "detail": "Credenciales incorrectas"
}
```

### 1.2. Registrar Administrador (/api/v1/auth/register-admin)

> **Importante**: Este endpoint requiere autenticación como superusuario.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "email": "nuevo_admin@smartacademy.com",
  "password": "password123",
  "full_name": "Nuevo Administrador",
  "phone": "1234567890",
  "direction": "Calle Principal 123",
  "birth_date": "1990-01-01",
  "gender": "male"
}
```

**Notas sobre el campo `gender`:**
- Usar "male", "female" o "other" (en minúsculas)
- Si se envía en mayúsculas ("MALE", "FEMALE", "OTHER"), se convertirá automáticamente

**Response Exitosa (201 Created):**
```json
{
  "id": 2,
  "email": "nuevo_admin@smartacademy.com",
  "full_name": "Nuevo Administrador",
  "phone": "1234567890",
  "direction": "Calle Principal 123",
  "birth_date": "1990-01-01",
  "gender": "male",
  "role": "administrator",
  "photo": null,
  "is_active": true,
  "is_superuser": true
}
```

**Response Fallida (400 Bad Request):**
```json
{
  "detail": "El correo electrónico ya está registrado"
}
```

**Response Fallida (401 Unauthorized):**
```json
{
  "detail": "No se pudieron validar las credenciales"
}
```

**Response Fallida (403 Forbidden):**
```json
{
  "detail": "El usuario no tiene suficientes permisos"
}
```

### 1.3. Obtener Perfil del Usuario (/api/v1/auth/users/me/)

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "email": "admin@smartacademy.com",
  "full_name": "Administrador",
  "phone": "1234567890",
  "direction": "Calle Principal 123",
  "birth_date": "1990-01-01",
  "gender": "male",
  "role": "administrator",
  "photo": null,
  "is_active": true,
  "is_superuser": true
}
```

### 1.4. Cambiar Contraseña (/api/v1/auth/change-password)

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "current_password": "password_actual",
  "new_password": "nueva_password"
}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Contraseña actualizada correctamente"
}
```

**Response Fallida (400 Bad Request):**
```json
{
  "detail": "Contraseña actual incorrecta"
}
```

## 2. Consejos para Evitar Bad Requests

### 2.1. Formato de Datos

- **Email**: Debe ser un email válido (ejemplo: `usuario@dominio.com`)
- **Contraseñas**: Se recomienda usar contraseñas de al menos 8 caracteres
- **Género**: Usar valores "male", "female" o "other" (en minúsculas) 
- **Roles**: Los valores válidos son "administrator", "teacher", "student", "parent" (en minúsculas)
- **Fechas**: Formato recomendado: "YYYY-MM-DD" (ejemplo: "1990-01-01")

### 2.2. Autenticación

- Siempre incluir el header `Authorization: Bearer {token}` en las peticiones que requieren autenticación
- El token tiene un tiempo de expiración (30 minutos), después del cual es necesario obtener uno nuevo mediante login

### 2.3. Problemas Comunes

- **401 Unauthorized**: Verifica que el token sea válido y no haya expirado
- **403 Forbidden**: El usuario no tiene los permisos necesarios (ejemplo: un usuario regular intentando registrar administradores)
- **400 Bad Request**: Verifica que el formato del JSON sea correcto y que los campos obligatorios estén presentes

### 2.4. Manejo de Enums

- Los enums como `gender` y `role` se almacenan en minúsculas en la base de datos
- Si envías valores en mayúsculas ("MALE", "FEMALE", "ADMINISTRATOR"), serán convertidos automáticamente
- Si no estás seguro del formato, siempre usa los valores en minúsculas como se indica en la documentación

## 3. Gestión de Usuarios

### 3.1. Crear Usuario (/api/v1/users/)

> **Importante**: Este endpoint requiere autenticación como superusuario.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "email": "profesor@smartacademy.com",
  "password": "password123",
  "full_name": "Profesor Ejemplo",
  "phone": "9876543210",
  "direction": "Calle Secundaria 456",
  "birth_date": "1985-05-15",
  "gender": "male",
  "role": "teacher",
  "is_superuser": false
}
```

**Response Exitosa (201 Created):**
```json
{
  "id": 3,
  "email": "profesor@smartacademy.com",
  "full_name": "Profesor Ejemplo",
  "phone": "9876543210",
  "direction": "Calle Secundaria 456",
  "birth_date": "1985-05-15",
  "gender": "male",
  "role": "teacher",
  "photo": null,
  "is_active": true,
  "is_superuser": false
}
```

### 3.2. Listar Usuarios (/api/v1/users/)

> **Importante**: Este endpoint requiere autenticación como superusuario.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros a devolver

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "email": "admin@smartacademy.com",
    "full_name": "Administrador",
    "phone": "1234567890",
    "direction": "Calle Principal 123",
    "birth_date": "1990-01-01",
    "gender": "male",
    "role": "administrator",
    "photo": null,
    "is_active": true,
    "is_superuser": true
  },
  {
    "id": 3,
    "email": "profesor@smartacademy.com",
    "full_name": "Profesor Ejemplo",
    "phone": "9876543210",
    "direction": "Calle Secundaria 456",
    "birth_date": "1985-05-15",
    "gender": "male",
    "role": "teacher",
    "photo": null,
    "is_active": true,
    "is_superuser": false
  }
]
```

### 3.3. Obtener Usuario por ID (/api/v1/users/{user_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Notas**: Un usuario regular solo puede ver su propio perfil. Los administradores pueden ver cualquier perfil.

**Response Exitosa (200 OK):**
```json
{
  "id": 3,
  "email": "profesor@smartacademy.com",
  "full_name": "Profesor Ejemplo",
  "phone": "9876543210",
  "direction": "Calle Secundaria 456",
  "birth_date": "1985-05-15",
  "gender": "male",
  "role": "teacher",
  "photo": null,
  "is_active": true,
  "is_superuser": false
}
```

### 3.4. Actualizar Usuario (/api/v1/users/{user_id})

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
```

**Notas**: Un usuario regular solo puede actualizar su propio perfil. Los administradores pueden actualizar cualquier perfil.

**Request:**
```json
{
  "full_name": "Profesor Ejemplo Actualizado",
  "phone": "9876543210",
  "direction": "Nueva Dirección 789",
  "birth_date": "1985-05-15",
  "gender": "male",
  "photo": "https://ejemplo.com/foto-profesor.jpg"
}
```

**Request (solo administradores, con campos adicionales):**
```json
{
  "full_name": "Profesor Ejemplo Actualizado",
  "phone": "9876543210",
  "direction": "Nueva Dirección 789",
  "birth_date": "1985-05-15",
  "gender": "male",
  "photo": "https://ejemplo.com/foto-profesor.jpg",
  "role": "teacher",
  "is_active": true
}
```

> **Importante**: 
> - Asegúrate de que el JSON sea válido. No incluyas una coma después del último elemento del objeto JSON.
> - El campo `photo` acepta una URL como string.
> - Solo los administradores pueden actualizar los campos `role` e `is_active`.

**Response Exitosa (200 OK):**
```json
{
  "id": 3,
  "email": "profesor@smartacademy.com",
  "full_name": "Profesor Ejemplo Actualizado",
  "phone": "9876543210",
  "direction": "Nueva Dirección 789",
  "birth_date": "1985-05-15",
  "gender": "male",
  "role": "teacher",
  "photo": null,
  "is_active": true,
  "is_superuser": false
}
```

### 3.5. Eliminar Usuario (/api/v1/users/{user_id})

> **Importante**: Este endpoint requiere autenticación como superusuario.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Usuario eliminado correctamente"
}
```

### 3.6. Obtener Roles de un Usuario (/api/v1/users/{user_id}/roles)

> **Nota**: Este endpoint permite consultar los roles de un usuario. Aunque conceptualmente se relaciona con la gestión de roles, su implementación se encuentra en el módulo de gestión de usuarios (`user.py`).

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Permisos**: Cualquier usuario autenticado puede acceder a este endpoint.

**Response Exitosa (200 OK) (Ejemplo para un usuario con múltiples roles):**
```json
[
  {
    "id": 1,
    "name": "student",
    "description": "Rol para estudiantes"
  },
  {
    "id": 3,
    "name": "editor",
    "description": "Rol con permisos de edición"
  }
]
```

**Response Exitosa (200 OK) (Ejemplo para un usuario sin roles adicionales o solo el rol por defecto):**
```json
[]
```

**Response Fallida (404 Not Found) (Si el `user_id` no existe):**
```json
{
  "detail": "Usuario no encontrado"
}
```

## 4. Gestión de Calificaciones (Grades)

### 4.1. Crear Calificación (/api/v1/grades/)

> **Importante**: Este endpoint requiere autenticación como profesor o administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "student_id": 1,
  "course_id": 2,
  "period": "Primer trimestre",
  "value": 85.5,
  "date_recorded": "2025-05-15"
}
```

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "student_id": 1,
  "course_id": 2,
  "period": "Primer trimestre",
  "value": 85.5,
  "date_recorded": "2025-05-15"
}
```

**Response Fallida (400 Bad Request):**
```json
{
  "detail": "El valor de la calificación debe estar entre 0 y 100"
}
```

**Response Fallida (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

### 4.2. Listar Calificaciones (/api/v1/grades/)

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `student_id`: Filtrar por ID de estudiante
- `course_id`: Filtrar por ID de curso
- `period`: Filtrar por periodo académico
- `date_from`: Filtrar por fecha de registro (desde)
- `date_to`: Filtrar por fecha de registro (hasta)
- `min_value`: Filtrar por valor mínimo de calificación
- `max_value`: Filtrar por valor máximo de calificación
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros a devolver

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "course_id": 2,
    "period": "Primer trimestre",
    "value": 85.5,
    "date_recorded": "2025-05-15"
  },
  {
    "id": 2,
    "student_id": 2,
    "course_id": 2,
    "period": "Primer trimestre",
    "value": 92.0,
    "date_recorded": "2025-05-16"
  }
]
```

### 4.3. Obtener Detalle de Calificación (/api/v1/grades/{grade_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "student_name": "Juan Pérez",
  "course_id": 2,
  "subject_name": "Matemáticas",
  "teacher_name": "Profesor Ejemplo",
  "group_name": "3ro A Primaria",
  "period": "Primer trimestre",
  "value": 85.5,
  "date_recorded": "2025-05-15"
}
```

### 4.4. Actualizar Calificación (/api/v1/grades/{grade_id})

> **Importante**: Este endpoint requiere autenticación como profesor asignado al curso o administrador.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "value": 88.0,
  "period": "Primer trimestre",
  "date_recorded": "2025-05-17"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "course_id": 2,
  "period": "Primer trimestre",
  "value": 88.0,
  "date_recorded": "2025-05-17"
}
```

### 4.5. Eliminar Calificación (/api/v1/grades/{grade_id})

> **Importante**: Este endpoint requiere autenticación como profesor asignado al curso o administrador.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Calificación eliminada correctamente"
}
```

## 5. Gestión de Asistencia (Attendance)

### 5.1. Registrar Asistencia (/api/v1/attendance/)

> **Importante**: Este endpoint requiere autenticación como profesor o administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "student_id": 1,
  "course_id": 2,
  "date": "2025-05-20",
  "status": "presente",
  "notes": "Llegó puntual"
}
```

> **Nota**: Los valores válidos para `status` son: "presente", "ausente", "tarde", "justificado" (en minúsculas)

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "student_id": 1,
  "course_id": 2,
  "date": "2025-05-20",
  "status": "presente",
  "notes": "Llegó puntual"
}
```

### 5.2. Listar Registros de Asistencia (/api/v1/attendance/)

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `student_id`: Filtrar por ID de estudiante
- `course_id`: Filtrar por ID de curso
- `date_from`: Filtrar por fecha (desde)
- `date_to`: Filtrar por fecha (hasta)
- `status`: Filtrar por estado de asistencia
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros a devolver

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "course_id": 2,
    "date": "2025-05-20",
    "status": "presente",
    "notes": "Llegó puntual"
  },
  {
    "id": 2,
    "student_id": 2,
    "course_id": 2,
    "date": "2025-05-20",
    "status": "tarde",
    "notes": "Llegó 10 minutos tarde"
  }
]
```

### 5.3. Obtener Detalle de Asistencia (/api/v1/attendance/{attendance_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "student_name": "Juan Pérez",
  "course_id": 2,
  "subject_name": "Matemáticas",
  "teacher_name": "Profesor Ejemplo",
  "group_name": "3ro A Primaria",
  "date": "2025-05-20",
  "status": "presente",
  "notes": "Llegó puntual"
}
```

### 5.4. Actualizar Registro de Asistencia (/api/v1/attendance/{attendance_id})

> **Importante**: Este endpoint requiere autenticación como profesor asignado al curso o administrador.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "status": "justificado",
  "notes": "Presentó justificante médico"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "course_id": 2,
  "date": "2025-05-20",
  "status": "justificado",
  "notes": "Presentó justificante médico"
}
```

### 5.5. Eliminar Registro de Asistencia (/api/v1/attendance/{attendance_id})

> **Importante**: Este endpoint requiere autenticación como profesor asignado al curso o administrador.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Registro de asistencia eliminado correctamente"
}
```

### 5.6. Estadísticas de Asistencia por Curso (/api/v1/attendance/stats/course/{course_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `date_from`: Filtrar por fecha (desde)
- `date_to`: Filtrar por fecha (hasta)

**Response Exitosa (200 OK):**
```json
{
  "total_classes": 20,
  "present_count": 15,
  "absent_count": 2,
  "late_count": 2,
  "excused_count": 1,
  "attendance_rate": 80.0
}
```

### 5.7. Estadísticas de Asistencia por Estudiante en un Curso (/api/v1/attendance/stats/student/{student_id}/course/{course_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `date_from`: Filtrar por fecha (desde)
- `date_to`: Filtrar por fecha (hasta)

**Response Exitosa (200 OK):**
```json
{
  "total_classes": 20,
  "present_count": 18,
  "absent_count": 1,
  "late_count": 1,
  "excused_count": 0,
  "attendance_rate": 90.0
}
```

## 6. Gestión de Tutores

### 6.1. Asignar Tutor a Estudiante (/api/v1/tutors/)

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: POST

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "student_id": 1,
  "user_id": 5,
  "relationship": "parent",
  "notes": "Madre del estudiante"
}
```

**Valores permitidos para relationship:**
- `tutor`: Tutor académico
- `parent`: Padre/madre
- `partner`: Apoderado
- `other`: Otro tipo de relación

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "student_id": 1,
  "user_id": 5,
  "relationship": "parent",
  "notes": "Madre del estudiante"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (400 Bad Request):**
```json
{
  "detail": "Ya existe una relación tutor-estudiante con estos datos"
}
```

### 6.2. Obtener Tutores de un Estudiante (/api/v1/tutors/student/{student_id})

> **Importante**: Este endpoint requiere autenticación. Pueden acceder: administradores, profesores del estudiante, tutores del estudiante o el propio estudiante.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "user_id": 5,
    "relationship": "parent",
    "notes": "Madre del estudiante",
    "student_name": "Juan Pérez",
    "tutor_name": "María Pérez",
    "tutor_email": "maria@example.com",
    "tutor_phone": "1234567890"
  },
  {
    "id": 2,
    "student_id": 1,
    "user_id": 6,
    "relationship": "parent",
    "notes": "Padre del estudiante",
    "student_name": "Juan Pérez",
    "tutor_name": "Carlos Pérez",
    "tutor_email": "carlos@example.com",
    "tutor_phone": "0987654321"
  }
]
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para ver los tutores de este estudiante"
}
```

### 6.3. Obtener Estudiantes Asignados a un Tutor (/api/v1/tutors/user/{user_id})

> **Importante**: Este endpoint requiere autenticación. Solo pueden acceder: el propio usuario o administradores.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "user_id": 5,
    "relationship": "parent",
    "notes": "Madre del estudiante",
    "student_name": "Juan Pérez",
    "tutor_name": "María Pérez",
    "tutor_email": "maria@example.com",
    "tutor_phone": "1234567890"
  },
  {
    "id": 3,
    "student_id": 2,
    "user_id": 5,
    "relationship": "parent",
    "notes": "Madre del estudiante",
    "student_name": "Ana Pérez",
    "tutor_name": "María Pérez",
    "tutor_email": "maria@example.com",
    "tutor_phone": "1234567890"
  }
]
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para ver esta información"
}
```

### 6.4. Obtener Detalle de Relación Tutor-Estudiante (/api/v1/tutors/{tutor_id})

> **Importante**: Este endpoint requiere autenticación. Pueden acceder: administradores, profesores del estudiante, el tutor o el propio estudiante.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "user_id": 5,
  "relationship": "parent",
  "notes": "Madre del estudiante",
  "student_name": "Juan Pérez",
  "tutor_name": "María Pérez",
  "tutor_email": "maria@example.com",
  "tutor_phone": "1234567890"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Relación tutor-estudiante no encontrada"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para ver esta relación tutor-estudiante"
}
```

### 6.5. Actualizar Relación Tutor-Estudiante (/api/v1/tutors/{tutor_id})

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "relationship": "tutor",
  "notes": "Tutor académico asignado"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "user_id": 5,
  "relationship": "tutor",
  "notes": "Tutor académico asignado"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Relación tutor-estudiante no encontrada"
}
```

### 6.6. Eliminar Relación Tutor-Estudiante (/api/v1/tutors/{tutor_id})

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Relación tutor-estudiante eliminada correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Relación tutor-estudiante no encontrada"
}
```
## 7. Gestión de Roles

### 7.1. Crear Rol (/api/v1/roles/)

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "name": "moderator",
  "description": "Rol para moderadores de contenido"
}
```

**Response Exitosa (201 Created):**
```json
{
  "id": 4,
  "name": "moderator",
  "description": "Rol para moderadores de contenido"
}
```

**Response Fallida (400 Bad Request) (Si el rol ya existe):**
```json
{
  "detail": "El rol con este nombre ya existe"
}
```

### 7.2. Listar Roles (/api/v1/roles/)

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Permisos**: Cualquier usuario autenticado puede acceder.

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "name": "administrator",
    "description": "Rol de Administrador con todos los permisos"
  },
  {
    "id": 2,
    "name": "teacher",
    "description": "Rol para Profesores"
  },
  {
    "id": 3,
    "name": "student",
    "description": "Rol para Estudiantes"
  }
]
```

### 7.3. Obtener Rol por ID (/api/v1/roles/{role_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Permisos**: Cualquier usuario autenticado puede acceder.

**Response Exitosa (200 OK):**
```json
{
  "id": 2,
  "name": "teacher",
  "description": "Rol para Profesores"
}
```

**Response Fallida (404 Not Found):**
```json
{
  "detail": "Rol no encontrado"
}
```

### 7.4. Actualizar Rol (/api/v1/roles/{role_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request:**
```json
{
  "name": "teacher_level_2",
  "description": "Rol para Profesores con experiencia Nivel 2"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 2,
  "name": "teacher_level_2",
  "description": "Rol para Profesores con experiencia Nivel 2"
}
```

**Response Fallida (404 Not Found):**
```json
{
  "detail": "Rol no encontrado"
}
```

### 7.5. Eliminar Rol (/api/v1/roles/{role_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Rol eliminado correctamente"
}
```

**Response Fallida (404 Not Found):**
```json
{
  "detail": "Rol no encontrado"
}
```

### 7.6. Asignar Rol a Usuario (/api/v1/roles/{role_id}/assign_to_user/{user_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Rol asignado correctamente al usuario"
}
```

**Response Fallida (404 Not Found) (Rol o Usuario no encontrado):**
```json
{
  "detail": "Rol no encontrado" 
}
```

**Response Fallida (400 Bad Request) (Usuario ya tiene el rol):**
```json
{
  "detail": "El usuario ya tiene este rol asignado"
}
```

### 7.7. Remover Rol de Usuario (/api/v1/roles/{role_id}/remove_from_user/{user_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Rol removido correctamente del usuario"
}
```

**Response Fallida (404 Not Found) (Rol o Usuario no encontrado, o el usuario no tiene el rol):**
```json
{
  "detail": "Rol no encontrado" 
}
```


## 8. Gestión de Cursos

### 8.1. Crear Curso (/api/v1/courses/)

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Matemáticas Avanzadas",
  "description": "Curso de matemáticas para nivel avanzado.",
  "teacher_id": 2, 
  "period_id": 1,  
  "grade": "5to",
  "level": "secondary"
}
```

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "name": "Matemáticas Avanzadas",
  "description": "Curso de matemáticas para nivel avanzado.",
  "teacher_id": 2,
  "period_id": 1,
  "grade": "5to",
  "level": "secondary",
  "teacher_name": "Profesor Ejemplo",
  "period_name": "2024-2025"
}
```

**Response Error (404 Not Found) (Profesor o Periodo no encontrado):**
```json
{
  "detail": "Profesor no encontrado" 
}
```

### 8.2. Listar Cursos (/api/v1/courses/)

> **Importante**: Cualquier usuario autenticado puede acceder.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `teacher_id`: Filtrar por ID de profesor.
- `student_id`: Filtrar por ID de estudiante (mostrará cursos donde el estudiante está inscrito). (**Pendiente de Implementación**)
- `period_id`: Filtrar por ID de periodo académico.
- `grade`: Filtrar por grado.
- `level`: Filtrar por nivel.

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Matemáticas Avanzadas",
    "description": "Curso de matemáticas para nivel avanzado.",
    "teacher_id": 2,
    "period_id": 1,
    "grade": "5to",
    "level": "secondary",
    "teacher_name": "Profesor Ejemplo",
    "period_name": "2024-2025"
  },
  {
    "id": 2,
    "name": "Historia Universal",
    "description": "Curso de historia universal.",
    "teacher_id": 3,
    "period_id": 1,
    "grade": "4to",
    "level": "secondary",
    "teacher_name": "Otro Profesor",
    "period_name": "2024-2025"
  }
]
```

### 8.3. Obtener Curso por ID (/api/v1/courses/{course_id})

> **Importante**: Cualquier usuario autenticado puede acceder.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "name": "Matemáticas Avanzadas",
  "description": "Curso de matemáticas para nivel avanzado.",
  "teacher_id": 2,
  "period_id": 1,
  "grade": "5to",
  "level": "secondary",
  "teacher_name": "Profesor Ejemplo",
  "period_name": "2024-2025"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Curso no encontrado"
}
```

### 8.4. Actualizar Curso (/api/v1/courses/{course_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Matemáticas Super Avanzadas",
  "description": "Curso de matemáticas para nivel super avanzado y genios.",
  "teacher_id": 4 
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "name": "Matemáticas Super Avanzadas",
  "description": "Curso de matemáticas para nivel super avanzado y genios.",
  "teacher_id": 4,
  "period_id": 1, 
  "grade": "5to",   
  "level": "secondary", 
  "teacher_name": "Nuevo Profesor Genio",
  "period_name": "2024-2025"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Curso no encontrado"
}
```

### 8.5. Eliminar Curso (/api/v1/courses/{course_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Curso eliminado correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Curso no encontrado"
}
```

### 8.6. Inscribir Estudiantes en un Curso (/api/v1/courses/{course_id}/students)

> **Importante**: Este endpoint requiere autenticación como Administrador.
> **Estado: Pendiente de Implementación.**

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "student_ids": [10, 12, 15] 
}
```

**Response Exitosa (200 OK) (Ejemplo):**
```json
{
  "message": "Estudiantes inscritos correctamente en el curso.",
  "details": {
    "course_id": 1,
    "students_added_count": 3,
    "students_already_in_course_count": 0,
    "students_not_found_count": 0
  }
}
```

**Response Error (404 Not Found) (Curso no encontrado):**
```json
{
  "detail": "Curso no encontrado"
}
```

### 8.7. Remover Estudiante de un Curso (/api/v1/courses/{course_id}/students/{student_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.
> **Estado: Pendiente de Implementación.**

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK) (Ejemplo):**
```json
{
  "message": "Estudiante removido correctamente del curso."
}
```

**Response Error (404 Not Found) (Curso o Estudiante no encontrado, o Estudiante no inscrito):**
```json
{
  "detail": "Estudiante no encontrado en este curso."
}
```

### 8.8. Listar Estudiantes de un Curso (/api/v1/courses/{course_id}/students)

> **Importante**: Profesores del curso y Administradores pueden acceder.
> **Estado: Pendiente de Implementación.**

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK) (Ejemplo):**
```json
[
  {
    "id": 10,
    "first_name": "Ana",
    "last_name": "Gomez",
    "email": "ana.gomez@example.com"
  },
  {
    "id": 12,
    "first_name": "Luis",
    "last_name": "Martinez",
    "email": "luis.martinez@example.com"
  }
]
```

**Response Error (404 Not Found) (Curso no encontrado):**
```json
{
  "detail": "Curso no encontrado"
}
```


# Ejemplos de Peticiones JSON para Smart Academy API - Fase 4

## 9. Gestión de Matrículas y Pagos

### 9.1. Registrar Matrícula/Pago (/api/v1/tuitions/)

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: POST

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "student_id": 1,
  "amount": 150.00,
  "month": "september",
  "year": 2025,
  "status": "paid",
  "description": "Matrícula mensual",
  "payment_date": "2025-05-15",
  "due_date": null
}
```

**Valores permitidos para status:**
- `paid`: Pago completado
- `pending`: Pago pendiente
- `overdue`: Pago vencido

**Valores permitidos para month:**
- `january`, `february`, `march`, `april`, `may`, `june`, `july`, `august`, `september`, `october`, `november`, `december`

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "student_id": 1,
  "amount": 150.00,
  "month": "september",
  "year": 2025,
  "status": "paid",
  "description": "Matrícula mensual",
  "payment_date": "2025-05-15",
  "due_date": null,
  "created_at": "2025-05-15"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (400 Bad Request):**
```json
{
  "detail": "Ya existe un registro de pago para este estudiante en september de 2025"
}
```

### 9.2. Obtener Pagos de un Estudiante (/api/v1/tuitions/student/{student_id})

> **Importante**: Este endpoint requiere autenticación. Pueden acceder: administradores, tutores del estudiante o el propio estudiante.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Parámetros de consulta opcionales:**
- `status`: Filtrar por estado ("paid", "pending", "overdue")
- `year`: Filtrar por año

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "amount": 150.00,
    "month": "september",
    "year": 2025,
    "status": "paid",
    "description": "Matrícula mensual",
    "payment_date": "2025-05-15",
    "due_date": null,
    "created_at": "2025-05-15",
    "student_name": "Juan Pérez",
    "student_code": "EST-001",
    "group_name": "1A"
  },
  {
    "id": 2,
    "student_id": 1,
    "amount": 150.00,
    "month": "october",
    "year": 2025,
    "status": "pending",
    "description": "Matrícula mensual",
    "payment_date": null,
    "due_date": "2025-10-05",
    "created_at": "2025-05-20",
    "student_name": "Juan Pérez",
    "student_code": "EST-001",
    "group_name": "1A"
  }
]
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para ver los pagos de este estudiante"
}
```

### 9.3. Obtener Detalle de Matrícula/Pago (/api/v1/tuitions/{tuition_id})

> **Importante**: Este endpoint requiere autenticación. Pueden acceder: administradores, tutores del estudiante o el propio estudiante.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "amount": 150.00,
  "month": "september",
  "year": 2025,
  "status": "paid",
  "description": "Matrícula mensual",
  "payment_date": "2025-05-15",
  "due_date": null,
  "created_at": "2025-05-15",
  "student_name": "Juan Pérez",
  "student_code": "EST-001",
  "group_name": "1A"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Matrícula/pago no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para ver este pago"
}
```

### 9.4. Actualizar Matrícula/Pago (/api/v1/tuitions/{tuition_id})

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "amount": 175.00,
  "status": "paid",
  "description": "Matrícula mensual + cargo por mora",
  "payment_date": "2025-05-20"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "student_id": 1,
  "amount": 175.00,
  "month": "september",
  "year": 2025,
  "status": "paid",
  "description": "Matrícula mensual + cargo por mora",
  "payment_date": "2025-05-20",
  "due_date": null,
  "created_at": "2025-05-15"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Matrícula/pago no encontrado"
}
```

### 9.5. Eliminar Matrícula/Pago (/api/v1/tuitions/{tuition_id})

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Matrícula/pago eliminado correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Matrícula/pago no encontrado"
}
```


### 9.6. Listar Matrículas/Pagos de un Estudiante (/api/v1/students/{student_id}/tuitions)

> **Corresponde a**: CU15 en `README.md`
> **Importante**: Este endpoint requiere autenticación. Pueden acceder: administradores, el propio estudiante y sus tutores legales.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Parámetros de Path:**
- `student_id` (integer, obligatorio): ID del estudiante.

**Parámetros de consulta opcionales:**
- `status`: Filtrar por estado ("paid", "pending", "overdue")
- `year`: Filtrar por año (ej. 2025)
- `month`: Filtrar por mes (ej. "september")
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros a devolver

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "student_id": 1,
    "amount": 150.00,
    "month": "september",
    "year": 2025,
    "status": "paid",
    "description": "Matrícula mensual Septiembre",
    "payment_date": "2025-09-05",
    "due_date": "2025-09-10",
    "created_at": "2025-09-01T10:00:00Z",
    "updated_at": "2025-09-05T11:30:00Z"
  },
  {
    "id": 2,
    "student_id": 1,
    "amount": 150.00,
    "month": "october",
    "year": 2025,
    "status": "pending",
    "description": "Matrícula mensual Octubre",
    "payment_date": null,
    "due_date": "2025-10-10",
    "created_at": "2025-10-01T10:00:00Z",
    "updated_at": "2025-10-01T10:00:00Z"
  }
]
```

**Response Error (404 Not Found - Estudiante no encontrado):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para acceder a las matrículas de este estudiante."
}
```

## 10. Gestión de Notificaciones

### 10.1. Crear Notificación (/api/v1/notifications/)

> **Importante**: Los usuarios regulares solo pueden crear notificaciones para sí mismos. Los administradores pueden crear notificaciones para cualquier usuario.

**Método**: POST

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "title": "Recordatorio de Examen",
  "content": "Se le recuerda que el examen de Matemáticas será mañana a las 10:00 AM",
  "type": "academic",
  "priority": "high",
  "recipient_id": 5,
  "sender_id": 1
}
```

**Valores permitidos para type:**
- `system`: Notificación del sistema
- `academic`: Notificación académica
- `payment`: Notificación de pago
- `attendance`: Notificación de asistencia
- `grade`: Notificación de calificaciones
- `general`: Notificación general

**Valores permitidos para priority:**
- `low`: Prioridad baja
- `medium`: Prioridad media
- `high`: Prioridad alta
- `urgent`: Prioridad urgente

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "title": "Recordatorio de Examen",
  "content": "Se le recuerda que el examen de Matemáticas será mañana a las 10:00 AM",
  "type": "academic",
  "priority": "high",
  "recipient_id": 5,
  "sender_id": 1,
  "is_read": false,
  "created_at": "2025-05-20T14:30:00",
  "read_at": null
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Usuario destinatario no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para crear notificaciones para otros usuarios"
}
```

### 10.2. Crear Notificaciones Masivas (/api/v1/notifications/bulk)

> **Importante**: Este endpoint solo puede ser utilizado por administradores.

**Método**: POST

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "recipient_ids": [1, 2, 3, 4, 5],
  "title": "Aviso General",
  "content": "Se suspenden las clases el día viernes por asamblea de profesores",
  "type": "general",
  "priority": "medium"
}
```

**Response Exitosa (201 Created):**
```json
{
  "message": "Se han creado 5 notificaciones correctamente",
  "count": 5
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Los siguientes IDs de usuario no existen: {2, 6}"
}
```

### 10.3. Obtener Notificaciones de un Usuario (/api/v1/notifications/user/{user_id})

> **Importante**: Los usuarios solo pueden ver sus propias notificaciones. Los administradores pueden ver las notificaciones de cualquier usuario.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Parámetros de consulta opcionales:**
- `is_read`: Filtrar por estado de lectura (true/false)
- `type`: Filtrar por tipo
- `priority`: Filtrar por prioridad
- `skip`: Para paginación
- `limit`: Para paginación, máximo 50 por página

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Recordatorio de Examen",
    "content": "Se le recuerda que el examen de Matemáticas será mañana a las 10:00 AM",
    "type": "academic",
    "priority": "high",
    "recipient_id": 5,
    "sender_id": 1,
    "is_read": false,
    "created_at": "2025-05-20T14:30:00",
    "read_at": null,
    "recipient_name": "Juan Pérez",
    "sender_name": "Admin Sistema"
  },
  {
    "id": 2,
    "title": "Aviso General",
    "content": "Se suspenden las clases el día viernes por asamblea de profesores",
    "type": "general",
    "priority": "medium",
    "recipient_id": 5,
    "sender_id": 1,
    "is_read": true,
    "created_at": "2025-05-19T10:15:00",
    "read_at": "2025-05-19T10:20:00",
    "recipient_name": "Juan Pérez",
    "sender_name": "Admin Sistema"
  }
]
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para ver las notificaciones de este usuario"
}
```

### 10.4. Marcar Notificación como Leída (/api/v1/notifications/{notification_id}/read)

> **Importante**: Los usuarios solo pueden marcar sus propias notificaciones. Los administradores pueden marcar las notificaciones de cualquier usuario.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "title": "Recordatorio de Examen",
  "content": "Se le recuerda que el examen de Matemáticas será mañana a las 10:00 AM",
  "type": "academic",
  "priority": "high",
  "recipient_id": 5,
  "sender_id": 1,
  "is_read": true,
  "created_at": "2025-05-20T14:30:00",
  "read_at": "2025-05-20T15:45:00"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Notificación no encontrada"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para marcar esta notificación"
}
```

### 10.5. Eliminar Notificación (/api/v1/notifications/{notification_id})

> **Importante**: Los usuarios solo pueden eliminar sus propias notificaciones. Los administradores pueden eliminar las notificaciones de cualquier usuario.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Notificación eliminada correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Notificación no encontrada"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para eliminar esta notificación"
}
```

## 11. Predicción y Análisis de Rendimiento Académico

### 11.1. Entrenar Modelo de Predicción (/api/v1/predictions/train)

> **Importante**: Este endpoint requiere autenticación como administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {token}
```

**Parametros Query:**
```
model_type: "random_forest" | "linear_regression" | "gradient_boosting"
advanced: true | false
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Modelo random_forest entrenado correctamente",
  "details": {
    "timestamp": "2025-06-03T01:25:12",
    "features_used": ["attendance_rate", "participation_score", "grade_trend", "attendance_trend"],
    "cross_validation_scores": [0.83, 0.79, 0.81, 0.77, 0.80],
    "mean_accuracy": 0.80,
    "model_file": "rf_model_20250603_012512.joblib"
  }
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permisos para esta acción"
}
```

**Response Error (400 Bad Request):**
```json
{
  "detail": "Tipo de modelo no válido, opciones: random_forest, linear_regression, gradient_boosting"
}
```

### 11.2. Predecir Rendimiento de Estudiante (/api/v1/predictions/student/{student_id})

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Parametros Path:**
```
student_id: int
```

**Parametros Query (opcionales):**
```
course_id: int | null
advanced: true | false
```

**Response Exitosa - Modo Básico (200 OK):**
```json
{
  "student_id": 5,
  "full_name": "María López",
  "predicted_grade": 78.5,
  "performance_category": "alto",
  "attendance_rate": 95.0,
  "participation_score": 8.5
}
```

**Response Exitosa - Modo Avanzado (200 OK):**
```json
{
  "student_id": 5,
  "full_name": "María López",
  "predictions": [
    {
      "course_id": 2,
      "course_name": "Matemáticas",
      "predicted_grade": 82.5,
      "performance_category": "alto",
      "risk_level": "Bajo",
      "risk_factors": ["Ninguno significativo"],
      "attendance_rate": 97.5,
      "participation_score": 9.0,
      "grade_trend": 0.8,
      "attendance_trend": 0.1,
      "recommendations": ["Mantener el excelente nivel de participación y asistencia"]
    },
    {
      "course_id": 3,
      "course_name": "Física",
      "predicted_grade": 75.0,
      "performance_category": "medio",
      "risk_level": "Medio",
      "risk_factors": ["Tendencia negativa en calificaciones", "Participación decreciente"],
      "attendance_rate": 92.0,
      "participation_score": 7.2,
      "grade_trend": -0.5,
      "attendance_trend": 0.0,
      "recommendations": ["Aumentar la participación en clase", "Buscar tutorías adicionales"]
    }
  ],
  "overall_risk": "Bajo",
  "analysis_date": "2025-06-03T01:30:45"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (400 Bad Request):**
```json
{
  "error": "No hay datos suficientes para generar una predicción"
}
```

### 9.3. Estadísticas para Dashboard (/api/v1/predictions/dashboard/stats)

> **Importante**: Este endpoint requiere autenticación como profesor o administrador.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "total_predictions": 120,
  "unique_students": 35,
  "performance_distribution": {
    "alto": 42,
    "medio": 58,
    "bajo": 20
  },
  "risk_level_distribution": {
    "Alto": 15,
    "Medio": 25,
    "Bajo": 80
  },
  "common_risk_factors": [
    ["Baja asistencia", 18],
    ["Participación decreciente", 15],
    ["Tendencia negativa en calificaciones", 12],
    ["Entrega tardía de tareas", 8],
    ["Inasistencia a exámenes", 5]
  ],
  "correlations": {
    "attendance_performance": 0.78,
    "participation_performance": 0.85
  }
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permisos para acceder a las estadísticas de predicciones"
}
```

### 9.4. Estudiantes en Riesgo (/api/v1/predictions/at-risk)

> **Importante**: Este endpoint requiere autenticación como profesor o administrador.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Parametros Query (opcionales):**
```
risk_level: "Alto" | "Medio" | "Bajo"
limit: int
```

**Response Exitosa (200 OK):**
```json
{
  "risk_level": "Alto",
  "count": 3,
  "at_risk_students": [
    {
      "student_id": 12,
      "full_name": "Carlos Martínez",
      "course_id": 2,
      "course_name": "Matemáticas",
      "predicted_grade": 48.5,
      "performance_category": "bajo",
      "risk_level": "Alto",
      "risk_factors": ["Baja asistencia", "No participación", "Tendencia negativa en calificaciones"],
      "attendance_rate": 65.0,
      "participation_score": 3.2,
      "grade_trend": -1.2
    },
    {
      "student_id": 8,
      "full_name": "Ana García",
      "course_id": 4,
      "course_name": "Química",
      "predicted_grade": 52.0,
      "performance_category": "bajo",
      "risk_level": "Alto",
      "risk_factors": ["Inasistencia a exámenes", "Participación decreciente"],
      "attendance_rate": 72.0,
      "participation_score": 4.5,
      "grade_trend": -0.9
    },
    {
      "student_id": 17,
      "full_name": "Roberto Sanchez",
      "course_id": 5,
      "course_name": "Historia",
      "predicted_grade": 55.5,
      "performance_category": "medio",
      "risk_level": "Alto",
      "risk_factors": ["Entrega tardía de tareas", "Tendencia negativa en calificaciones"],
      "attendance_rate": 80.0,
      "participation_score": 6.0,
      "grade_trend": -1.5
    }
  ]
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permisos para acceder a esta información"
}
```


## 12. Gestión de Periodos Académicos

### 12.1. Crear Periodo Académico (/api/v1/periods/)

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Año Escolar 2025-2026",
  "start_date": "2025-09-01",
  "end_date": "2026-06-30",
  "status": "planned"
}
```
**Notas sobre el campo `status`:**
- Valores permitidos: "planned", "active", "completed", "archived" (en minúsculas).

**Response Exitosa (201 Created):**
```json
{
  "id": 3,
  "name": "Año Escolar 2025-2026",
  "start_date": "2025-09-01",
  "end_date": "2026-06-30",
  "status": "planned"
}
```

**Response Error (400 Bad Request) (Fechas inválidas o nombre duplicado):**
```json
{
  "detail": "La fecha de inicio no puede ser posterior a la fecha de fin."
}
```
```json
{
  "detail": "Ya existe un periodo académico con este nombre."
}
```

### 12.2. Listar Periodos Académicos (/api/v1/periods/)

> **Importante**: Cualquier usuario autenticado puede acceder.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `status`: Filtrar por estado ("planned", "active", "completed", "archived").
- `skip`: Número de registros a omitir (paginación).
- `limit`: Número máximo de registros a devolver.

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Año Escolar 2023-2024",
    "start_date": "2023-09-01",
    "end_date": "2024-06-30",
    "status": "completed"
  },
  {
    "id": 2,
    "name": "Año Escolar 2024-2025",
    "start_date": "2024-09-01",
    "end_date": "2025-06-30",
    "status": "active"
  }
]
```

### 12.3. Obtener Periodo Académico por ID (/api/v1/periods/{period_id})

> **Importante**: Cualquier usuario autenticado puede acceder.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 2,
  "name": "Año Escolar 2024-2025",
  "start_date": "2024-09-01",
  "end_date": "2025-06-30",
  "status": "active"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Periodo académico no encontrado"
}
```

### 12.4. Actualizar Periodo Académico (/api/v1/periods/{period_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Año Escolar 2024-2025 (Actualizado)",
  "status": "active",
  "end_date": "2025-07-15"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 2,
  "name": "Año Escolar 2024-2025 (Actualizado)",
  "start_date": "2024-09-01",
  "end_date": "2025-07-15",
  "status": "active"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Periodo académico no encontrado"
}
```

**Response Error (400 Bad Request) (Nombre duplicado o fechas inválidas):**
```json
{
  "detail": "Ya existe otro periodo académico con este nombre."
}
```

### 12.5. Eliminar Periodo Académico (/api/v1/periods/{period_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Periodo académico eliminado correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Periodo académico no encontrado"
}
```

**Response Error (400 Bad Request) (Periodo tiene cursos asociados):**
```json
{
  "detail": "No se puede eliminar el periodo académico porque tiene cursos asociados."
}
```
```


## 13. Gestión de Asignaturas

### 13.1. Crear Asignatura (/api/v1/subjects/)

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Matemáticas Discretas",
  "description": "Estudio de estructuras matemáticas fundamentales para la computación.",
  "area": "Ciencias Exactas"
}
```

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "name": "Matemáticas Discretas",
  "description": "Estudio de estructuras matemáticas fundamentales para la computación.",
  "area": "Ciencias Exactas"
}
```

**Response Error (400 Bad Request) (Nombre duplicado):**
```json
{
  "detail": "Ya existe una asignatura con este nombre."
}
```

### 13.2. Listar Asignaturas (/api/v1/subjects/)

> **Importante**: Cualquier usuario autenticado puede acceder.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `area`: Filtrar por área de conocimiento.
- `skip`: Número de registros a omitir (paginación).
- `limit`: Número máximo de registros a devolver.

**Response Exitosa (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Matemáticas Discretas",
    "description": "Estudio de estructuras matemáticas fundamentales para la computación.",
    "area": "Ciencias Exactas"
  },
  {
    "id": 2,
    "name": "Programación Orientada a Objetos",
    "description": "Principios y paradigmas de la POO.",
    "area": "Tecnología"
  }
]
```

### 13.3. Obtener Asignatura por ID (/api/v1/subjects/{subject_id})

> **Importante**: Cualquier usuario autenticado puede acceder.
> **Nota**: Este endpoint no está explícitamente en CU4 del README, pero es una práctica común para CRUD.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "name": "Matemáticas Discretas",
  "description": "Estudio de estructuras matemáticas fundamentales para la computación.",
  "area": "Ciencias Exactas"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Asignatura no encontrada"
}
```

### 13.4. Actualizar Asignatura (/api/v1/subjects/{subject_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.
> **Nota**: Este endpoint no está explícitamente en CU4 del README, pero es una práctica común para CRUD.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Matemáticas Discretas Avanzadas",
  "description": "Estudio avanzado de estructuras matemáticas discretas y sus aplicaciones.",
  "area": "Ciencias Exactas y Computación"
}
```

**Response Exitosa (200 OK):**
```json
{
  "id": 1,
  "name": "Matemáticas Discretas Avanzadas",
  "description": "Estudio avanzado de estructuras matemáticas discretas y sus aplicaciones.",
  "area": "Ciencias Exactas y Computación"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Asignatura no encontrada"
}
```

### 13.5. Eliminar Asignatura (/api/v1/subjects/{subject_id})

> **Importante**: Este endpoint requiere autenticación como Administrador.
> **Nota**: Este endpoint no está explícitamente en CU4 del README, pero es una práctica común para CRUD.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Asignatura eliminada correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Asignatura no encontrada"
}
```

**Response Error (400 Bad Request) (Asignatura tiene cursos asociados o criterios):**
```json
{
  "detail": "No se puede eliminar la asignatura porque tiene cursos o criterios de evaluación asociados."
}
```

### 13.6. Crear Subcriterio de Evaluación para Asignatura (/api/v1/subjects/{subject_id}/subcriteria)

> **Importante**: Este endpoint requiere autenticación como Administrador.

**Método**: POST

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "Examen Parcial 1",
  "description": "Primer examen parcial de la asignatura.",
  "max_value": 25.0,
  "main_criterion_id": 1 
}
```
**Nota**: `main_criterion_id` se referiría a un criterio principal de evaluación previamente definido (ej. "Exámenes", "Proyectos", etc.). La gestión de Criterios Principales podría ser otra sección o estar implícita. Para este ejemplo, se asume que existe.

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "name": "Examen Parcial 1",
  "description": "Primer examen parcial de la asignatura.",
  "max_value": 25.0,
  "subject_id": 1,
  "main_criterion_id": 1
}
```

**Response Error (404 Not Found) (Asignatura o Criterio Principal no encontrado):**
```json
{
  "detail": "Asignatura no encontrada" 
}
```
```json
{
  "detail": "Criterio principal de evaluación no encontrado"
}
```
```


## 14. Gestión de Reportes Académicos y Dashboards

Esta sección combina endpoints de CU10 (Gestión de reportes académicos) y endpoints de dashboard del sistema de predicción.

### 14.1. Obtener Estadísticas Generales del Dashboard (/api/v1/dashboard/stats)

> **Corresponde a**: CU10 en `README.md`
> **Importante**: Este endpoint requiere autenticación como Administrador o Profesor.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "total_students": 1500,
  "active_courses": 45,
  "average_attendance_rate": 0.92,
  "overall_average_grade": 8.5,
  "teachers_count": 75,
  "pending_tasks": 12 
}
```
**Nota**: La estructura y campos de la respuesta son ejemplos y pueden variar.

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permisos para acceder a estas estadísticas."
}
```

### 14.2. Obtener Reporte Individual del Estudiante para Dashboard (/api/v1/dashboard/student/{student_id})

> **Corresponde a**: CU10 en `README.md`
> **Importante**: Requiere autenticación. Administradores, Profesores (del estudiante), el propio Estudiante y sus Padres pueden acceder.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "student_info": {
    "id": 123,
    "full_name": "Ana Pérez García",
    "email": "ana.perez@example.com",
    "current_grade_level": "5to Primaria"
  },
  "academic_summary": {
    "average_grade": 9.1,
    "attendance_rate": 0.95,
    "courses_enrolled": 8,
    "recent_achievements": ["Ganadora Concurso Ortografía", "Mejor Promedio Trimestre 1"]
  },
  "performance_prediction": {
    "risk_level": "Bajo",
    "predicted_average_grade": 9.0,
    "positive_factors": ["Alta participación", "Excelente asistencia"],
    "areas_for_improvement": ["Matemáticas (Ejercicios prácticos)"]
  },
  "alerts": [] 
}
```
**Nota**: La estructura y campos de la respuesta son ejemplos y pueden variar.

**Response Error (404 Not Found):**
```json
{
  "detail": "Estudiante no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permisos para acceder al reporte de este estudiante."
}
```

### 14.3. Obtener Estadísticas de Predicciones para Dashboard (/api/v1/predictions/dashboard/stats)

> **Corresponde a**: Endpoints de Predicción en `README.md`
> **Importante**: Este endpoint requiere autenticación como Administrador o Profesor.

**Método**: GET

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response Exitosa (200 OK):**
```json
{
  "total_predictions_made": 5670,
  "model_accuracy": {
    "overall": 0.88,
    "last_training_cycle": 0.90
  },
  "students_at_risk": {
    "high": 15,
    "medium": 45,
    "low": 120
  },
  "most_influential_factors": ["attendance_rate", "previous_grades", "participation_score"]
}
```
**Nota**: La estructura y campos de la respuesta son ejemplos y pueden variar.

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permisos para acceder a estas estadísticas de predicción."
}
```
```
