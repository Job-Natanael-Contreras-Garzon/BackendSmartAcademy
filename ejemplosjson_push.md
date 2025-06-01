# Ejemplos de Peticiones JSON para Notificaciones Push

## 1. Registro de Dispositivos

### 1.1. Registrar Dispositivo (/api/v1/devices/)

> **Importante**: Este endpoint requiere autenticación. Cada usuario solo puede registrar sus propios dispositivos.

**Método**: POST

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "device_token": "fMdnrJ6CSo2OsW0yx-PrM7:APA91bGhRTzMEWqg...",
  "device_platform": "android",
  "device_name": "Mi Xiaomi Redmi Note 10"
}
```

**Valores permitidos para device_platform:**
- `android`: Dispositivos Android
- `ios`: Dispositivos iOS
- `web`: Aplicaciones web

**Response Exitosa (201 Created):**
```json
{
  "id": 1,
  "user_id": 5,
  "device_token": "fMdnrJ6CSo2OsW0yx-PrM7:APA91bGhRTzMEWqg...",
  "device_platform": "android",
  "device_name": "Mi Xiaomi Redmi Note 10",
  "created_at": "2025-06-01T14:30:00",
  "is_active": true
}
```

### 1.2. Obtener Dispositivos Registrados (/api/v1/devices/)

> **Importante**: Este endpoint requiere autenticación. Cada usuario solo puede ver sus propios dispositivos.

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
    "user_id": 5,
    "device_token": "fMdnrJ6CSo2OsW0yx-PrM7:APA91bGhRTzMEWqg...",
    "device_platform": "android",
    "device_name": "Mi Xiaomi Redmi Note 10",
    "created_at": "2025-06-01T14:30:00",
    "is_active": true
  },
  {
    "id": 2,
    "user_id": 5,
    "device_token": "dHFT7y6tGhUiO9p8L...",
    "device_platform": "ios",
    "device_name": "iPhone 13",
    "created_at": "2025-06-01T15:45:00",
    "is_active": true
  }
]
```

### 1.3. Eliminar Dispositivo (/api/v1/devices/{device_id})

> **Importante**: Este endpoint requiere autenticación. Cada usuario solo puede eliminar sus propios dispositivos.

**Método**: DELETE

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "message": "Dispositivo eliminado correctamente"
}
```

**Response Error (404 Not Found):**
```json
{
  "detail": "Dispositivo no encontrado"
}
```

**Response Error (403 Forbidden):**
```json
{
  "detail": "No tienes permiso para eliminar este dispositivo"
}
```

## 2. Preferencias de Notificaciones

### 2.1. Obtener Preferencias (/api/v1/devices/preferences)

> **Importante**: Este endpoint requiere autenticación. Cada usuario solo puede ver sus propias preferencias.

**Método**: GET

**Headers:**
```
Authorization: Bearer {token}
```

**Response Exitosa (200 OK):**
```json
{
  "enable_push": true,
  "enable_academic": true,
  "enable_payment": true,
  "enable_attendance": true,
  "enable_grade": true,
  "enable_general": true
}
```

### 2.2. Actualizar Preferencias (/api/v1/devices/preferences)

> **Importante**: Este endpoint requiere autenticación. Cada usuario solo puede actualizar sus propias preferencias.

**Método**: PUT

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Request:**
```json
{
  "enable_push": true,
  "enable_academic": true,
  "enable_payment": true,
  "enable_attendance": false,
  "enable_grade": true,
  "enable_general": true
}
```

**Response Exitosa (200 OK):**
```json
{
  "enable_push": true,
  "enable_academic": true,
  "enable_payment": true,
  "enable_attendance": false,
  "enable_grade": true,
  "enable_general": true
}
```

## 3. Notificaciones Push (Integración Flutter)

### Pasos para implementar en Flutter

1. Añadir las dependencias en `pubspec.yaml`:

```yaml
dependencies:
  firebase_core: ^2.4.0
  firebase_messaging: ^14.2.0
  flutter_local_notifications: ^13.0.0
```

2. Inicializar Firebase y solicitar permisos:

```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

// En el main o donde inicialices la app
Future<void> _initFirebase() async {
  await Firebase.initializeApp();
  
  // Solicitar permisos
  final settings = await FirebaseMessaging.instance.requestPermission(
    alert: true,
    announcement: false,
    badge: true,
    carPlay: false,
    criticalAlert: false,
    provisional: false,
    sound: true,
  );
  
  // Obtener token FCM
  final token = await FirebaseMessaging.instance.getToken();
  print('FCM Token: $token');
  
  // Registrar token en el backend
  if (token != null) {
    await registerDeviceToken(token);
  }
}
```

3. Función para registrar el token en el backend:

```dart
Future<void> registerDeviceToken(String token) async {
  final response = await http.post(
    Uri.parse('$apiBaseUrl/api/v1/devices/'),
    headers: {
      'Authorization': 'Bearer $authToken',
      'Content-Type': 'application/json'
    },
    body: jsonEncode({
      'device_token': token,
      'device_platform': Platform.isIOS ? 'ios' : 'android',
      'device_name': await _getDeviceName()
    }),
  );
  
  if (response.statusCode == 201) {
    print('Token registrado correctamente');
  } else {
    print('Error al registrar token: ${response.body}');
  }
}
```

4. Configurar manejadores de notificaciones:

```dart
void _setupFirebaseMessaging() {
  // Cuando la app está en primer plano
  FirebaseMessaging.onMessage.listen((RemoteMessage message) {
    print('Notificación recibida en primer plano: ${message.notification?.title}');
    // Mostrar notificación local
    _showLocalNotification(message);
  });

  // Cuando la app está en segundo plano y se hace tap en la notificación
  FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
    print('Notificación abierta desde segundo plano: ${message.notification?.title}');
    // Navegar a la pantalla correspondiente según el tipo de notificación
    _handleNotificationNavigation(message);
  });
}
```
