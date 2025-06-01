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
