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
# Ejemplos de Peticiones JSON para Smart Academy API - Fase 4

## 7. Gestión de Matrículas y Pagos

### 7.1. Registrar Matrícula/Pago (/api/v1/tuitions/)

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

### 7.2. Obtener Pagos de un Estudiante (/api/v1/tuitions/student/{student_id})

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

### 7.3. Obtener Detalle de Matrícula/Pago (/api/v1/tuitions/{tuition_id})

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

### 7.4. Actualizar Matrícula/Pago (/api/v1/tuitions/{tuition_id})

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

### 7.5. Eliminar Matrícula/Pago (/api/v1/tuitions/{tuition_id})

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

## 8. Gestión de Notificaciones

### 8.1. Crear Notificación (/api/v1/notifications/)

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

### 8.2. Crear Notificaciones Masivas (/api/v1/notifications/bulk)

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

### 8.3. Obtener Notificaciones de un Usuario (/api/v1/notifications/user/{user_id})

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

### 8.4. Marcar Notificación como Leída (/api/v1/notifications/{notification_id}/read)

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

### 8.5. Eliminar Notificación (/api/v1/notifications/{notification_id})

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


