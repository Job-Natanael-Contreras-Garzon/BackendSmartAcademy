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
